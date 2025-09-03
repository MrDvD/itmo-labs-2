package main

import (
	"encoding/json"
	"fmt"
	"mime"
	"net/http"
	"os"
	"path"
	"path/filepath"
	"strings"
)

type DotParams struct {
	X string `json:"X"`
	Y int    `json:"Y"`
	R string `json:"R"`
}

type DotStatus struct {
	Entry DotParams `json:"entry"`
}

func serveIndex(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "GET":
		data, err := os.ReadFile("./public/index.html")
		if err != nil {
			fmt.Println(err)
			return
		}
		w.Write(data)
	default:
		http.Error(w, "405 method not allowed", http.StatusMethodNotAllowed)
	}
}

func serveDotParams(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "POST":
		var dots []DotParams
		err := json.NewDecoder(r.Body).Decode(&dots)
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		var dotsStatus []DotStatus
		for _, dot := range dots {
			dotsStatus = append(dotsStatus, DotStatus{Entry: dot})
		}
		b, err := json.Marshal(dotsStatus)
		if err != nil {
			http.Error(w, "500 failure json serialization", http.StatusInternalServerError)
			return
		}
		w.Write(b)
	default:
		http.Error(w, "405 method not allowed", http.StatusMethodNotAllowed)
	}
}

func servePublic(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "GET":
		data, err := os.ReadFile("./public" + r.URL.Path)
		fileExtension := filepath.Ext(r.URL.Path)
		fileMimeType := mime.TypeByExtension(fileExtension)
		w.Header().Set("Content-type", fileMimeType)
		if err != nil {
			fmt.Println(err)
			return
		}
		w.Write(data)
	default:
		http.Error(w, "405 method not allowed", http.StatusMethodNotAllowed)
	}
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
	case "dot-params":
		serveDotParams(w, r)
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
