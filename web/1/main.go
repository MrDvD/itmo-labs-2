package main

import (
	"fmt"
	"mrdvd/lib"
	"net/http"
	"os"
)

func main() {
	domain, ok := os.LookupEnv("APP_DOMAIN")
	if !ok {
		fmt.Printf("APP_DOMAIN environment variable is not set!")
		return
	}
	port, ok := os.LookupEnv("APP_PORT")
	if !ok {
		fmt.Printf("APP_PORT environment variable is not set!")
		return
	}
	host := fmt.Sprintf("%s:%s", domain, port)
	s := &http.Server{
		Addr:    host,
		Handler: http.HandlerFunc(lib.Serve),
	}
	fmt.Printf("Starting server at %s\n", host)
	err := s.ListenAndServe()
	if err != nil {
		fmt.Println("Error starting the server:", err)
	}
}
