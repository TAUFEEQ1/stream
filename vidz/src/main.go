package main

import (
	"net/http"

	"github.com/gorilla/mux"
)

func serveFile() {
	//Notify analyzer for each
	//Segment being requested of the time
	//movie_id as well as user_id
	//record viewing session.
}
func main() {
	http.Handle("/", handlers())
	http.ListenAndServe(":8003", nil)
}
func handlers() *mux.Router {
	router := mux.NewRouter()
	router.HandleFunc("{segno}/{userId}/{videoId}/stream/", streamHandler).Methods("GET")
	return router
}
func streamHandler(response http.ResponseWriter, request *http.Request) {

}
