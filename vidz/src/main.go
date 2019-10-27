package main

import (
	"net/http"
	"strconv"
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

var db gorm.DB

func main() {
	db, err := gorm.Open("sqlite3", "../../flicks")
	if err != nil {
		panic("failed to connect database")
	}
	http.Handle("/", handlers())
	http.ListenAndServe(":8003", nil)
	defer db.Close()
}
func handlers() *mux.Router {
	router := mux.NewRouter()
	router.HandleFunc("{movieserial}/{userviewId}/{segno}/stream/", streamHandler).Methods("GET")
	return router
}
func streamHandler(response http.ResponseWriter, request *http.Request) {
	vars := mux.Vars(request)
	// Get all movie serial, segment_id
	thepath := "../public/" + vars["movieserial"] + "/segment_" + vars["segno"]
	userviewId, _ := strconv.Atoi(vars["userviewId"])
	segno, _ := strconv.Atoi(vars["segno"])
	recordView(userviewId, segno)
	serveFile(thepath, response, request)
}
func serveFile(thepath string, response http.ResponseWriter, request *http.Request) {
	http.ServeFile(response, request, thepath)
}
func recordView(userviewId int, segno int) {
	db.Create(&userviewlets{userviews_id: userviewId, segment: segno, created_at: time.Now()})
}
