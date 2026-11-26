from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    """Простой веб-сервер для отдачи HTML-страниц и приема POST-запросов."""

    def do_GET(self):
        pages = {
            "/": "templates/contacts.html",
            "/contacts": "templates/contacts.html",
            "/home": "templates/index.html",
            "/catalog": "templates/catalog.html",
            "/category": "templates/category.html",
        }

        try:
            file_path = pages.get(self.path)

            if file_path:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(bytes(content, "utf-8"))
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(bytes("<h1>404 — Страница не найдена</h1>", "utf-8"))
        except Exception as error:
            print(f"Ошибка сервера: {error}")
            self.send_response(500)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(bytes("<h1>500 — Внутренняя ошибка сервера</h1>", "utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        print("Получены данные POST-запроса:", parse_qs(post_data))

        with open("templates/contacts.html", "r", encoding="utf-8") as file:
            content = file.read()

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes(content, "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started http://{hostName}:{serverPort}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
