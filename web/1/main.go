package main

import (
	"fmt"
	"mime"
	"net/http"
	"os"
	"path"
	"path/filepath"
	"strings"
)

func serveIndex(w http.ResponseWriter, _ *http.Request) {
	data, err := os.ReadFile("./public/index.html")
	if err != nil {
		fmt.Println(err)
		return
	}
	w.Write(data)
}

func servePublic(w http.ResponseWriter, r *http.Request) {
	data, err := os.ReadFile("./public" + r.URL.Path)
	fileExtension := filepath.Ext(r.URL.Path)
	fileMimeType := mime.TypeByExtension(fileExtension)
	w.Header().Set("Content-type", fileMimeType)
	if err != nil {
		fmt.Println(err)
		return
	}
	w.Write(data)
}

func shiftPath(p string) (head, tail string) {
	p = path.Clean("/" + p)
	i := strings.Index(p[1:], "/") + 1
	if i <= 0 {
		return p[1:], "/"
	}
	return p[1:i], p[i:]
}

func serve(w http.ResponseWriter, r *http.Request) {
	var head string
	head, _ = shiftPath(r.URL.Path)
	switch head {
	case "":
		serveIndex(w, r)
	default:
		servePublic(w, r)
	}
}

func main() {
	s := &http.Server{
		Addr:    "localhost:8080",
		Handler: http.HandlerFunc(serve),
	}
	fmt.Println("Starting server at port 8080")
	err := s.ListenAndServe()
	if err != nil {
		fmt.Println("Error starting the server:", err)
	}
}
