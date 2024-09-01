export default {
  async fetch(request, env, ctx) {
    // Function for getting a request from the cache or going to origin.
    async function fetchCacheOrOrigin(request, ctx) {
      // Check if data is in cache
      const cacheUrl = new URL(request.url);
      const cacheKey = new Request(cacheUrl.toString());
      const cache = caches.default;
      let response = await cache.match(cacheKey);
      // Data is not in the cache already
      if (!response)
      {
        // Fetch the request.
        response = await fetch(request);
        console.log("Fetching Origin for Cache "+request.url);
        // Cache it
        response = new Response(response.body, response);
        ctx.waitUntil(cache.put(cacheKey, response.clone()));
      }
      else
        console.log("Data was in cache already for "+request.url);
  
      return response;
    }

    // Check if authorization is enabled
    const authRequired = (env.REQUIRE_AUTH == "true");
    if (authRequired === false) {
      return fetchCacheOrOrigin(request, ctx);
    }
    
    // Check for Auth Header
    const authHeader = request.headers.get("Authorization");
    if (authHeader != null) {
      // Extract API Key
      const tokenCheck = authHeader.toString().replace("Bearer ", "");
      // Check if it exists
      let task = await env.TOKEN_LIST.get(tokenCheck);
      
      // Key is valid!
      if (task)
        return await fetchCacheOrOrigin(request, ctx);
    }

    // Incorrect key supplied. Reject the request.
    return new Response(JSON.stringify({msg: "you have provided an invalid key", status: false}), {
      status: 403,
      headers: new Headers({"content-type": "application/json"})
    });
  },
};
