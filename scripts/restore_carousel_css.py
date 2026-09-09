from pathlib import Path

path = Path('styles.css')
css = path.read_text(encoding='utf-8')
marker = '/* ===== HOME PROMO CAROUSEL ===== */'

if marker in css:
    print('Carousel CSS already present.')
    raise SystemExit(0)

block = r'''

/* ===== HOME PROMO CAROUSEL ===== */
.home-carousel {
  position: relative;
  width: calc(100% - 36px);
  max-width: 1320px;
  aspect-ratio: 2560 / 1000;
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
}

.home-carousel-prev { left: 10px; }
.home-carousel-next { right: 10px; }

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
  background: #fff;
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

  .home-carousel-prev { left: 6px; }
  .home-carousel-next { right: 6px; }

  .home-carousel-dots {
    bottom: 7px;
    gap: 6px;
  }

  .home-carousel-dots button {
    width: 6px;
    height: 6px;
  }

  .home-carousel-dots button.active { width: 18px; }
}
'''

path.write_text(css + block, encoding='utf-8')
print('Carousel CSS restored.')
