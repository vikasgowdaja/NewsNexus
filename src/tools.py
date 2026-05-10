import os
import json
import urllib.parse
import urllib.request
from langchain.tools import tool
from langchain_ollama import ChatOllama
from vector_store import retrieve_documents

# --- Tool 1: The RAG Tool (Enhanced with Deep Links) ---
@tool
def lookup_policy_docs(query: str) -> str:
    """
    Useful for finding specific details, statistics, or sections from the uploaded 
    industry reports (PDFs). Use this when you need factual grounding.
    """
    # Clean the query if it comes in as a dictionary string
    if isinstance(query, str) and "{" in query:
        query = query.replace("{", "").replace("}", "").replace("value:", "")
        
    docs = retrieve_documents(query, k=3)
    if not docs:
        return f"RAG: No relevant internal documents found for query: '{query}'."
        
    results = []
    for doc, score in docs:
        source_name = doc.metadata.get('source', 'Unknown PDF')
        basename = os.path.basename(source_name)
        safe_source_path = source_name.replace('\\', '/')
        results.append(f"Content: {doc.page_content}\nSource Link: [{basename}](file:///{safe_source_path})")
    
    return "\n\n".join(results)

# --- Tool 2: The Live Web Search Tool (Enhanced with Citations) ---
@tool
def web_search_stub(query: str) -> str:
    """
    Useful for finding the 'latest' or 'current' news from the internet.
    Use this for recent trends, real-time events, or any information not in the PDFs.
    """
    from duckduckgo_search import DDGS
    import re
    
    clean_query = str(query)
    if "{" in clean_query:
        match = re.search(r'["\']query["\']:\s*["\']([^"\']+)["\']', clean_query)
        if match:
            clean_query = match.group(1)
        else:
            clean_query = clean_query.replace("{", "").replace("}", "").replace("value:", "").strip()

    print(f"\n[Tool Called] Live Web Search for: '{clean_query}'")
    
    backend_errors = []
    empty_backends = []
    backends = ["lite", "html"]

    for backend in backends:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(clean_query, max_results=10, backend=backend))

            if results:
                formatted_results = []
                for res in results:
                    title = res.get("title", "Source")
                    link = res.get("href", res.get("url", "#"))
                    snippet = res.get("body", res.get("snippet", "No Snippet"))
                    formatted_results.append(f"Title: {title}\nLink: [{title}]({link})\nSnippet: {snippet}")
                return "\n\n---\n".join(formatted_results)

            empty_backends.append(backend)
        except Exception as e:
            backend_errors.append(f"{backend}: {e}")

    # Additional fallback: DuckDuckGo news search can return results
    # even when general text search returns empty.
    try:
        with DDGS() as ddgs:
            news_results = list(ddgs.news(clean_query, max_results=10))

        if news_results:
            formatted_news = []
            for res in news_results:
                title = res.get("title", "Source")
                link = res.get("url", "#")
                snippet = res.get("body", res.get("excerpt", "No Snippet"))
                formatted_news.append(f"Title: {title}\nLink: [{title}]({link})\nSnippet: {snippet}")
            return "\n\n---\n".join(formatted_news)
    except Exception as e:
        backend_errors.append(f"news: {e}")

    # Last fallback: return curated RSS findings when live search is blocked.
    rss_fallback = rss_feed_search.invoke(clean_query)
    if rss_fallback and not str(rss_fallback).startswith("No matching recent RSS entries found"):
        return f"WEB: Live DuckDuckGo search unavailable. Using RSS fallback data.\n\n{rss_fallback}"

    # Entity fallback: if web backends are blocked/empty, try Wikipedia summary.
    # This avoids false conclusions like "topic has low coverage" for well-known entities.
    wiki_title = urllib.parse.quote(clean_query.replace(" ", "_"))
    wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{wiki_title}"
    try:
        req = urllib.request.Request(
            wiki_url,
            headers={"User-Agent": "NewsNexus/1.0 (research-assistant)"},
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            payload = json.loads(resp.read().decode("utf-8"))

        extract = payload.get("extract")
        page_url = payload.get("content_urls", {}).get("desktop", {}).get("page", "https://en.wikipedia.org")
        title = payload.get("title", clean_query)
        if extract:
            return (
                "WEB: Live DuckDuckGo results unavailable/empty. "
                "Using Wikipedia entity fallback.\n\n"
                f"Title: {title}\n"
                f"Link: [{title}]({page_url})\n"
                f"Snippet: {extract}"
            )
    except Exception as e:
        backend_errors.append(f"wikipedia: {e}")

    # If we reached here, distinguish between outage and "no matches found".
    # Empty results are a normal search outcome and should not be treated as outage.
    if backend_errors and not empty_backends:
        return (
            "WEB: Search temporarily unavailable. "
            "Treat this as a retrieval outage, not as factual evidence about the topic. "
            f"Debug detail: {' | '.join(backend_errors)}"
        )

    if empty_backends or backend_errors:
        debug_parts = []
        if empty_backends:
            debug_parts.append(f"empty backends: {', '.join(empty_backends)}")
        if backend_errors:
            debug_parts.append(f"errors: {' | '.join(backend_errors)}")
        debug_msg = " ; ".join(debug_parts) if debug_parts else "no debug details"

        return (
            "WEB: No matching live web results found for this query right now. "
            "Treat this as low external coverage for the exact query, not as an outage. "
            f"Debug detail: {debug_msg}"
        )

    return (
        "WEB: Search temporarily unavailable. "
        "Treat this as a retrieval outage, not as factual evidence about the topic. "
        f"Debug detail: {' | '.join(backend_errors)}"
    )

# --- Tool 3: RSS Feed Connector (Enhanced) ---
@tool
def rss_feed_search(query: str) -> str:
    """
    Useful for finding high-quality, targeted news from specific industry RSS feeds.
    """
    import feedparser
    
    FEEDS = [
        "https://www.technologyreview.com/feed/",
        "https://openai.com/news/rss.xml",
        "https://machinelearning.apple.com/rss.xml",
        "https://feeds.feedburner.com/TheHackersNews",
        "https://techcrunch.com/feed/"
    ]
    
    results = []
    # Broaden keyword search
    keywords = query.lower().split()
    print(f"\n[Tool Called] RSS Search for keywords: {keywords}")
    
    for url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                text_to_search = (entry.title + " " + entry.get("summary", "")).lower()
                # Match if ANY keyword exists (Hybrid match)
                if any(kw in text_to_search for kw in keywords):
                    results.append(f"Source: {feed.feed.get('title', 'Industry News')}\nTitle: {entry.title}\nLink: [{entry.title}]({entry.link})\nSummary: {entry.get('summary', '')[:250]}...")
        except Exception as e:
            continue
            
    return "\n\n---\n".join(results) if results else "No matching recent RSS entries found."

def get_llm_with_tools():
    llm = ChatOllama(model="llama3.2", temperature=0) 
    tools = [lookup_policy_docs, web_search_stub, rss_feed_search]
    llm_with_tools = llm.bind_tools(tools)
    return llm, llm_with_tools, tools

if __name__ == "__main__":
    # Test Block
    base_llm, agent, tools_list = get_llm_with_tools()
    query = "Latest AI models by Apple or OpenAI"
    print(f"Testing tools... {query}")
    print(agent.invoke(query).tool_calls)
