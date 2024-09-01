# AntiScamBotAPI
API for querying ScamBot via HTTP Get.

This allows you to have a publicly accessible API to your [AntiScamBot](https://github.com/SocksTheWolf/AntiScamBot) installation.

## Setup

This setup assumes you know how to [setup a python virtual environment already](https://fastapi.tiangolo.com/virtual-environments/).

Clone the project somewhere that can access your AntiScamBot database file, and then create an .env with the following information

```
DATABASE_FILE="PATH TO DATABASE FILE
```
Run with `fastapi run` or via the run script in the `.runtime` folder.

## Authentication

Authorization is not natively provided, and in the case of the public ScamGuard application is executed via Cloudflare workers. Below is the script that is used on the public ScamGuard instance. You will have to set up your own bindings and KV Database for handling authentication.

```
export default {
  async fetch(request, env, ctx) {
    // Check if authorization is enabled
    const authRequired = (env.REQUIRE_AUTH == "true");
    if (authRequired === false) {
      return fetch(request);
    }
    
    const authHeader = request.headers.get("Authorization");
    if (authHeader != null) {
      const tokenCheck = authHeader.toString().replace("Bearer ", "");
      let task = await env.TOKEN_LIST.get(tokenCheck);
      
      // Key is valid!
      if (task) {
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
          console.log("Fetching for Cache "+request.url);
          // Cache it
          response = new Response(response.body, response);
          ctx.waitUntil(cache.put(cacheKey, response.clone()));
        }
        else
          console.log("Data was in cache already for "+request.url);
        
        return response;
      }
    }

    // Incorrect key supplied. Reject the request.
    return new Response("Sorry, you have supplied an invalid key.", {
      status: 403,
    });
  },
};
```

Auth keys do not expire (as they're really only implemented to prevent misuse).
