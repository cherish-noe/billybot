
def scrape_web(apify_client, url, depth):

    # Prepare the Actor input
    run_input = {
        "startUrls": [{ "url": url }],
        "includeUrlGlobs": [],
        "excludeUrlGlobs": [],
        "maxCrawlDepth": int(depth),
        "initialCookies": [],
        "proxyConfiguration": { "useApifyProxy": True },
        "removeElementsCssSelector": """nav, footer, script, style, noscript, svg,
    [role=\"alert\"],
    [role=\"banner\"],
    [role=\"dialog\"],
    [role=\"alertdialog\"],
    [role=\"region\"][aria-label*=\"skip\" i],
    [aria-modal=\"true\"]""",
        "clickElementsCssSelector": "[aria-expanded=\"false\"]",
    }

    # Run the Actor and wait for it to finish
    run = apify_client.actor("apify/website-content-crawler").call(run_input=run_input)
    return run, apify_client