https://channels.readthedocs.io/en/latest/introduction.html
https://chatgpt.com/share/69010a5e-7270-8006-aee5-7ce51d976351

# Channels extend Django abilities beyond HTTP - to handle WebSockets.
# Use Cases : 
    - chat protocols, IoT protocols and notification but it no longer used (ENG. Abdelrahman advise).

# built on a Python specification called ASGI.
# Whilst Django still handles traditional HTTP, Channels gives you the choice to handle other connections in either a synchronous or asynchronous style.

# Channels is comprised of several packages:

     -Channels, the Django integration layer

     -Daphne, the HTTP and Websocket termination server

     -asgiref, the base ASGI library

     -channels_redis, the Redis channel layer backend (optional)


# In regular projects, Django typically runs on Gunicorn or uWSGI, which handle HTTP requests only (synchronous).
# However, when using Django Channels to support WebSockets, you need to use Daphne as the ASGI server instead of WSGI.

Daphane/Uvicorn --> ASGI  , Gunicorn/uWSGI --> WSGI


فلسفة Channels إن كل حاجة عبارة عن تطبيق ASGI مستقل.
حتى الـ Consumer الصغير (اللي زي الـ View في Django) -هو في حد ذاته تطبيق ASGI كامل ممكن تشغله لوحده.


السيرفر بيعرف منين إن الاتصال لسه مفتوح؟

الجميل في WebSocket إن البروتوكول نفسه بيهتم بالموضوع ده.
الاتصال بيكون عبارة عن “قناة ثنائية الاتجاه” بين العميل والسيرفر،
والاتنين بيعملوا حاجة اسمها heartbeat / ping-pong كل فترة صغيرة.
وده كله بيحصل تلقائي في طبقة WebSocket (مش لازم تبرمجه بنفسك).