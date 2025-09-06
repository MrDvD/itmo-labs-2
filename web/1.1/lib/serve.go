package lib

import (
	"encoding/json"
	"fmt"
	"io"
	"mime"
	"net/http"
	"os"
	"path"
	"path/filepath"
	"strings"

	"github.com/graphql-go/graphql"
)

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

func serveGraphql(w http.ResponseWriter, r *http.Request) {
	schema, err := GetSchemaConfig()
	if err != nil {
		http.Error(w, "500 graphql schema failure", http.StatusInternalServerError)
		return
	}
	buf := new(strings.Builder)
	_, err = io.Copy(buf, r.Body)
	if err != nil {
		http.Error(w, "500 request read failure", http.StatusInternalServerError)
		return
	}
	params := graphql.Params{Schema: schema, RequestString: buf.String()}
	queryResult := graphql.Do(params)
	if len(queryResult.Errors) > 0 {
		http.Error(w, "500 graphql response failure", http.StatusInternalServerError)
		return
	}
	// var dots []DotParams
	// err := json.NewDecoder(r.Body).Decode(&dots)
	// if err != nil {
	// 	http.Error(w, err.Error(), http.StatusBadRequest)
	// 	return
	// }
	// var dotsStatuses []DotStatus
	// for _, dot := range dots {
	// 	dotStatus, err := wrapDotStatus(dot)
	// 	if err != nil {
	// 		http.Error(w, "400 bad request", http.StatusBadRequest)
	// 		return
	// 	}
	// 	dotsStatuses = append(dotsStatuses, dotStatus)
	// }
	b, err := json.Marshal(queryResult)
	if err != nil {
		http.Error(w, "500 failure json serialization", http.StatusInternalServerError)
		return
	}
	w.Write(b)
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

func Serve(w http.ResponseWriter, r *http.Request) {
	var head string
	head, _ = shiftPath(r.URL.Path)
	switch head {
	case "":
		serveIndex(w, r)
	case "graphql":
		serveGraphql(w, r)
	default:
		servePublic(w, r)
	}
}
