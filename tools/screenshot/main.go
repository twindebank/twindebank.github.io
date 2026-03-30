package main

import (
	"context"
	"flag"
	"log"
	"os"
	"time"

	"github.com/chromedp/chromedp"
)

func main() {
	url := flag.String("url", "http://localhost:8080/cv.html", "URL to screenshot")
	out := flag.String("out", "screenshot.png", "Output file path")
	width := flag.Int("width", 1200, "Viewport width")
	flag.Parse()

	ctx, cancel := chromedp.NewContext(context.Background())
	defer cancel()

	ctx, cancel = context.WithTimeout(ctx, 15*time.Second)
	defer cancel()

	var buf []byte
	err := chromedp.Run(ctx,
		chromedp.EmulateViewport(int64(*width), 900),
		chromedp.Navigate(*url),
		chromedp.WaitVisible("#content h1", chromedp.ByQuery),
		chromedp.FullScreenshot(&buf, 90),
	)
	if err != nil {
		log.Fatalf("screenshot failed: %v", err)
	}

	if err := os.WriteFile(*out, buf, 0644); err != nil {
		log.Fatalf("write failed: %v", err)
	}
	log.Printf("saved %s", *out)
}
