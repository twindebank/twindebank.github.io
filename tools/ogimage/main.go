package main

import (
	"context"
	"flag"
	"log"
	"net"
	"net/http"
	"os"
	"time"

	"github.com/chromedp/chromedp"
)

const htmlContent = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body {
  width: 1200px; height: 630px;
  background: #000 !important;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 80px;
  font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif;
}
h1 {
  font-size: 72px;
  font-weight: 100;
  letter-spacing: 12px;
  text-transform: uppercase;
  color: #fff;
  margin-bottom: 20px;
}
p {
  font-size: 20px;
  font-weight: 300;
  color: #555;
  letter-spacing: 3px;
  text-transform: uppercase;
}
.rule {
  width: 60px;
  height: 1px;
  background: #333;
  margin: 28px 0;
}
</style>
</head>
<body>
  <h1>Theo Windebank</h1>
  <div class="rule"></div>
  <p>Staff Engineer &nbsp;·&nbsp; Gradient Labs</p>
</body>
</html>`

func main() {
	out := flag.String("out", "og-image.png", "Output path")
	flag.Parse()

	ln, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		log.Fatalf("listen: %v", err)
	}
	srv := &http.Server{Handler: http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		w.Write([]byte(htmlContent))
	})}
	go srv.Serve(ln)
	defer srv.Close()

	url := "http://" + ln.Addr().String() + "/"

	ctx, cancel := chromedp.NewContext(context.Background())
	defer cancel()
	ctx, cancel = context.WithTimeout(ctx, 15*time.Second)
	defer cancel()

	var buf []byte
	err = chromedp.Run(ctx,
		chromedp.EmulateViewport(1200, 630),
		chromedp.Navigate(url),
		chromedp.Sleep(500*time.Millisecond),
		chromedp.CaptureScreenshot(&buf),
	)
	if err != nil {
		log.Fatalf("failed: %v", err)
	}
	if err := os.WriteFile(*out, buf, 0644); err != nil {
		log.Fatalf("write failed: %v", err)
	}
	log.Printf("saved %s", *out)
}
