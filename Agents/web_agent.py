# Agents/web_agent.py - بحث عبر DuckDuckGo Lite
import re
import requests
from bs4 import BeautifulSoup
import urllib.parse

def detect_language(text):
    if re.search(r'[ابتثجحخدذرزسشصضطظعغفقكلمنهوي]', text):
        return "ar"
    if re.search(r'[éèêëàâçôûïîœ]', text.lower()):
        return "fr"
    return "en"

def web_agent(state):
    print("🌐 Web Agent يعمل...")
    last_msg = state["messages"][-1].lower()
    lang = detect_language(last_msg)
    
    # كشف طلب البحث
    is_search = any(w in last_msg for w in ["ابحث", "search", "cherche", "بحث عن", "find", "trouve", "ما هو", "what is", "qu'est-ce que"])
    if not is_search:
        if lang == "ar":
            response = "🌐 أرسل `ابحث عن [موضوع]` للبحث على الإنترنت.\nمثال: ابحث عن آخر أخبار الذكاء الاصطناعي"
        elif lang == "fr":
            response = "🌐 Envoyez `cherche [sujet]` pour rechercher sur Internet.\nExemple: cherche actualités IA"
        else:
            response = "🌐 Send `search [topic]` to search the web.\nExample: search latest AI news"
        state["messages"].append(response)
        return state
    
    # استخراج كلمات البحث
    query = last_msg
    for w in ["ابحث", "search", "cherche", "بحث عن", "find", "trouve", "ما هو", "what is", "qu'est-ce que"]:
        query = query.replace(w, "").strip()
    if len(query) < 2:
        response = "⚠️ يرجى كتابة ما تريد البحث عنه." if lang == "ar" else "⚠️ Please enter a search query."
        state["messages"].append(response)
        return state
    
    state["messages"].append(f"🔍 جاري البحث عن: {query[:100]}...")
    
    # البحث عبر DuckDuckGo Lite
    try:
        url = f"https://lite.duckduckgo.com/lite/?q={urllib.parse.quote(query)}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        results = []
        # في صفحة lite، النتائج موجودة في جداول
        rows = soup.find_all('tr')
        current_result = {}
        for row in rows:
            if 'result-link' in row.get('class', []):
                link = row.find('a')
                if link:
                    current_result['href'] = link.get('href', '#')
                    current_result['title'] = link.text.strip()
            if 'result-snippet' in row.get('class', []):
                current_result['snippet'] = row.text.strip()
                results.append(current_result.copy())
                current_result = {}
        
        if results:
            response_lines = [f"🌐 **نتائج البحث عن: {query[:100]}**"]
            for res in results[:5]:
                title = res.get('title', '')
                snippet = res.get('snippet', '')
                href = res.get('href', '#')
                if len(snippet) > 200:
                    snippet = snippet[:200] + "..."
                response_lines.append(f"• **{title}**\n  {snippet}\n  🔗 {href}")
            response = "\n\n".join(response_lines)
        else:
            # محاولة البديل: البحث عبر HTML العادي
            alt_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
            resp2 = requests.get(alt_url, headers=headers, timeout=15)
            soup2 = BeautifulSoup(resp2.text, 'html.parser')
            for res in soup2.select('.result'):
                title_elem = res.select_one('.result__a')
                if title_elem:
                    title = title_elem.text.strip()
                    href = title_elem.get('href', '#')
                    snippet_elem = res.select_one('.result__snippet')
                    snippet = snippet_elem.text.strip() if snippet_elem else ""
                    if len(snippet) > 200:
                        snippet = snippet[:200] + "..."
                    results.append({'title': title, 'snippet': snippet, 'href': href})
            if results:
                response_lines = [f"🌐 **نتائج البحث عن: {query[:100]}**"]
                for res in results[:5]:
                    response_lines.append(f"• **{res['title']}**\n  {res['snippet']}\n  🔗 {res['href']}")
                response = "\n\n".join(response_lines)
            else:
                response = f"❌ لم يتم العثور على نتائج لـ: {query[:100]}." if lang == "ar" else f"❌ No results for: {query[:100]}."
    
    except Exception as e:
        print(f"⚠️ خطأ في البحث: {e}")
        response = f"❌ خطأ في البحث: {str(e)[:100]}" if lang == "ar" else f"❌ Search error: {str(e)[:100]}"
    
    state["messages"].append(response)
    return state
