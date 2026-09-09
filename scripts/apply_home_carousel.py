from pathlib import Path

INDEX_PATH = Path("index.html")
STYLES_PATH = Path("styles.css")

HTML_MARKER = "<!-- ===== HOME PROMO CAROUSEL ===== -->"
CSS_MARKER = "/* ===== HOME PROMO CAROUSEL ===== */"
JS_MARKER = "<!-- ===== HOME PROMO CAROUSEL SCRIPT ===== -->"

carousel_html = r'''

  <!-- ===== HOME PROMO CAROUSEL ===== -->
  <section class="home-carousel" id="homeCarousel" aria-label="Featured jewellery offers">
    <div class="home-carousel-track">
      <div class="home-carousel-slide active">
        <img src="carousel/banner-1.webp" alt="Jewellery for every story">
      </div>
      <div class="home-carousel-slide">
        <img src="carousel/banner-2.webp" alt="Moments shine brighter with gold">
      </div>
      <div class="home-carousel-slide">
        <img src="carousel/banner-3.webp" alt="Crafted for life's special moments">
      </div>
      <div class="home-carousel-slide">
        <img src="carousel/banner-4.webp" alt="Grace in every detail">
      </div>
      <div class="home-carousel-slide">
        <img src="carousel/banner-5.webp" alt="More than jewellery">
      </div>
    </div>

    <button class="home-carousel-arrow home-carousel-prev" type="button" aria-label="Previous banner">‹</button>
    <button class="home-carousel-arrow home-carousel-next" type="button" aria-label="Next banner">›</button>

    <div class="home-carousel-dots" aria-label="Choose banner">
      <button class="active" type="button" aria-label="Show banner 1"></button>
      <button type="button" aria-label="Show banner 2"></button>
      <button type="button" aria-label="Show banner 3"></button>
      <button type="button" aria-label="Show banner 4"></button>
      <button type="button" aria-label="Show banner 5"></button>
    </div>
  </section>
'''

carousel_css = r'''

/* ===== HOME PROMO CAROUSEL ===== */
.home-carousel {
  position: relative;
  width: calc(100% - 36px);
  max-width: 1320px;
  aspect-ratio: 1140 / 450;
  margin: 18px auto 0;
  overflow: hidden;
  border-radius: 18px;
  background: #111;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.18);
}

.home-carousel-track {
  position: relative;
  width: 100%;
  height: 100%;
}

.home-carousel-slide {
  position: absolute;
  inset: 0;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.75s ease, visibility 0.75s ease;
}

.home-carousel-slide.active {
  opacity: 1;
  visibility: visible;
  z-index: 1;
}

.home-carousel-slide img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}

.home-carousel-arrow {
  position: absolute;
  top: 50%;
  z-index: 4;
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  transform: translateY(-50%);
  border: 0;
  border-radius: 50%;
  background: rgba(15, 15, 15, 0.78);
  color: #e5c9f2;
  font-size: 2rem;
  line-height: 1;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.2s ease;
}

.home-carousel-arrow:hover {
  background: rgba(42, 24, 50, 0.94);
}

.home-carousel-prev {
  left: 10px;
}

.home-carousel-next {
  right: 10px;
}

.home-carousel-dots {
  position: absolute;
  left: 50%;
  bottom: 12px;
  z-index: 5;
  display: flex;
  gap: 8px;
  transform: translateX(-50%);
}

.home-carousel-dots button {
  width: 8px;
  height: 8px;
  padding: 0;
  border: 0;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.48);
  cursor: pointer;
  transition: width 0.25s ease, background 0.25s ease;
}

.home-carousel-dots button.active {
  width: 26px;
  background: #ffffff;
}

@media (max-width: 768px) {
  .home-carousel {
    width: calc(100% - 20px);
    margin-top: 10px;
    border-radius: 12px;
  }

  .home-carousel-arrow {
    width: 34px;
    height: 34px;
    font-size: 1.55rem;
  }

  .home-carousel-prev {
    left: 6px;
  }

  .home-carousel-next {
    right: 6px;
  }

  .home-carousel-dots {
    bottom: 7px;
    gap: 6px;
  }

  .home-carousel-dots button {
    width: 6px;
    height: 6px;
  }

  .home-carousel-dots button.active {
    width: 18px;
  }
}
'''

carousel_js = r'''

  <!-- ===== HOME PROMO CAROUSEL SCRIPT ===== -->
  <script>
    (() => {
      const carousel = document.getElementById('homeCarousel');
      if (!carousel) return;

      const slides = [...carousel.querySelectorAll('.home-carousel-slide')];
      const dots = [...carousel.querySelectorAll('.home-carousel-dots button')];
      const prev = carousel.querySelector('.home-carousel-prev');
      const next = carousel.querySelector('.home-carousel-next');
      let current = 0;
      let timer = null;
      const delay = 5000;

      const show = (index) => {
        current = (index + slides.length) % slides.length;
        slides.forEach((slide, i) => slide.classList.toggle('active', i === current));
        dots.forEach((dot, i) => dot.classList.toggle('active', i === current));
      };

      const stop = () => {
        if (timer) clearInterval(timer);
        timer = null;
      };

      const start = () => {
        stop();
        timer = setInterval(() => show(current + 1), delay);
      };

      prev?.addEventListener('click', () => {
        show(current - 1);
        start();
      });

      next?.addEventListener('click', () => {
        show(current + 1);
        start();
      });

      dots.forEach((dot, i) => {
        dot.addEventListener('click', () => {
          show(i);
          start();
        });
      });

      carousel.addEventListener('mouseenter', stop);
      carousel.addEventListener('mouseleave', start);

      let touchStartX = 0;
      carousel.addEventListener('touchstart', (event) => {
        touchStartX = event.changedTouches[0].clientX;
      }, { passive: true });

      carousel.addEventListener('touchend', (event) => {
        const delta = event.changedTouches[0].clientX - touchStartX;
        if (Math.abs(delta) > 45) {
          show(current + (delta < 0 ? 1 : -1));
          start();
        }
      }, { passive: true });

      show(0);
      start();
    })();
  </script>
'''

html = INDEX_PATH.read_text(encoding="utf-8")
if HTML_MARKER not in html:
    if "</header>" not in html:
        raise RuntimeError("Could not find </header> in index.html")
    html = html.replace("</header>", "</header>" + carousel_html, 1)

if JS_MARKER not in html:
    if "</body>" not in html:
        raise RuntimeError("Could not find </body> in index.html")
    html = html.replace("</body>", carousel_js + "\n</body>", 1)

INDEX_PATH.write_text(html, encoding="utf-8")

css = STYLES_PATH.read_text(encoding="utf-8")
if CSS_MARKER not in css:
    STYLES_PATH.write_text(css + carousel_css, encoding="utf-8")

print("Home promo carousel added below navigation.")
