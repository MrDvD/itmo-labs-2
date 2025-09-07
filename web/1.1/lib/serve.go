package lib

import (
	"encoding/json"
	"fmt"
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
		http.Error(w, "500 graphql schema init failure", http.StatusInternalServerError)
		return
	}
	var postData graphqlPostData
	err = json.NewDecoder(r.Body).Decode(&postData)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	params := graphql.Params{
		Schema:         schema,
		RequestString:  postData.Query,
		VariableValues: postData.Variables,
	}
	queryResult := graphql.Do(params)
	if len(queryResult.Errors) > 0 {
		fmt.Println(queryResult.Errors)
		http.Error(w, "400 graphql bad request", http.StatusBadRequest)
		return
	}
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
