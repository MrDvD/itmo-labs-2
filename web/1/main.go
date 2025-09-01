package main

import (
	"fmt"
	"net/http"
	"os"
)

func indexHandler(w http.ResponseWriter, r *http.Request) {
	data, err := os.ReadFile("./public/index.html")
	if err != nil {
		fmt.Println(err)
		return
	}
	w.Write(data)
}

func styleHandler(w http.ResponseWriter, r *http.Request) {
	data, err := os.ReadFile("./public/style.css")
	if err != nil {
		fmt.Println(err)
		return
	}
	w.Header().Add("Content-type", "text/css")
	w.Write(data)
}

func scriptHandler(w http.ResponseWriter, r *http.Request) {
	data, err := os.ReadFile("./public/script.js")
	if err != nil {
		fmt.Println(err)
		return
	}
	w.Header().Add("Content-type", "text/javascript")
	w.Write(data)
}

func main() {
	http.HandleFunc("/", indexHandler)
	http.HandleFunc("/style.css", styleHandler)
	http.HandleFunc("/script.js", scriptHandler)

	fmt.Println("Starting server at port 8080")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		fmt.Println("Error starting the server:", err)
	}
}
