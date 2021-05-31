# Easy client-side web analytics

they block google analytics but i'd bet they don't block this

## How to use

1. Get a MongoDB instance (perhaps on Atlas) and retrieve a connection string.
2. Set the connection string as the environment variable `PVT_MONGODB`
3. Install the requirements.txt and run the Flask server on the same origin as your website (for example, add it to your Vercel api directory). It can be running at any path, so long as you know what that path is.
4. On each of your client side pages, add this line of code somewhere: `fetch("<server path>", {method:'POST', body:window.location.href, credentials:'include'}).then(response=>response.text().then(status=>{if(status=="unconfirmed"){ fetch("<server path>", {method:'POST', body:window.location.href, credentials:'include'})}}));`
Be sure to replace both instances of `<server path>` with the path your server is running at.