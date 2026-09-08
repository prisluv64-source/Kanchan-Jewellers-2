const categories = [
  {name:'Gold Jewellery', sub:'Rings, chains, necklaces & more'},
  {name:'Silver Jewellery', sub:'Elegant everyday silver pieces'},
  {name:'Bridal', sub:'Wedding sets & statement pieces'},
  {name:'Rings', sub:'Classic and contemporary designs'},
  {name:'Earrings', sub:'Studs, drops & traditional designs'},
  {name:'Chains', sub:'Daily wear & occasion chains'},
  {name:'Bangles', sub:'Traditional and modern bangles'},
  {name:'Payal', sub:'Graceful silver anklets'}
];

const products = [
  {name:'Royal Gold Necklace', meta:'22K Gold • Sample product', tag:'Featured'},
  {name:'Classic Gold Ring', meta:'22K Gold • Sample product', tag:'New'},
  {name:'Heritage Jhumka', meta:'22K Gold • Sample product', tag:'Bestseller'},
  {name:'Silver Payal Pair', meta:'925 Silver • Sample product', tag:'Popular'},
  {name:'Bridal Choker Set', meta:'22K Gold • Sample product', tag:'Bridal'},
  {name:'Everyday Gold Chain', meta:'22K Gold • Sample product', tag:'Classic'}
];

document.querySelector('#categoryGrid').innerHTML = categories.map(c => `
  <article class="category-card">
    <div class="category-art"></div>
    <h3>${c.name}</h3><p>${c.sub}</p>
  </article>`).join('');

document.querySelector('#productGrid').innerHTML = products.map(p => `
  <article class="product-card">
    <div class="product-image"><div class="product-jewel"></div></div>
    <div class="product-body">
      <span class="tag">${p.tag}</span>
      <h3>${p.name}</h3>
      <div class="meta">${p.meta}</div>
      <div class="product-actions"><span>Price on enquiry</span><span class="enquire">Details coming soon</span></div>
    </div>
  </article>`).join('');

document.querySelector('#year').textContent = new Date().getFullYear();
document.querySelector('#menuBtn').addEventListener('click',()=>document.querySelector('#navMenu').classList.toggle('open'));
document.querySelectorAll('#navMenu a').forEach(a=>a.addEventListener('click',()=>document.querySelector('#navMenu').classList.remove('open')));
