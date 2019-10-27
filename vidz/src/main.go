package main

import (
	"net/http"
	"time"

	"github.com/gorilla/mux"
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/sqlite"
)

type userviewlets struct {
	gorm.Model
	userviews_id int
	segment      int
	created_at   time.Time
}

func recordView(userviewId, segno) {
	db.Model(&userviewlets{userviews_id: userviewId, segment: segno, created_at: time.Now()})
}
func main() {
	db, err := gorm.Open("sqlite3", "../../flicks")
	http.Handle("/", handlers())
	http.ListenAndServe(":8003", nil)
	defer db.Close()
}
func handlers() *mux.Router {
	router := mux.NewRouter()
	router.HandleFunc("{userviewId}/{segno}/stream/", streamHandler).Methods("GET")
	return router
}
func streamHandler(response http.ResponseWriter, request *http.Request) {

}
