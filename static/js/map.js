/* global fetch */

const mapDom = document.querySelector('.map')

let zoom = 1
let latestData = null

// zoom on scroll is working
// but turned off for now
// since it is conflicting with up and down navigation

// mapDom.addEventListener('wheel', (event) => {
//   // https://deepmikoto.com/coding/1--javascript-detect-mouse-wheel-direction
//   let delta = null
//   let direction = false
//   if (!event) { // if the event is not provided, we get it from the window object
//     event = window.event
//   }
//   if (event.wheelDelta) { // will work in most cases
//     delta = event.wheelDelta / 60
//   } else if (event.detail) { // fallback for Firefox
//     delta = -event.detail / 2
//   }
//   if (delta !== null) {
//     direction = delta > 0 ? 'up' : 'down'
//   }
//   if (direction === 'up') { // zoom in
//     zoom *= 1.1
//   } else { // zoom out
//     zoom *= 0.9
//   }
//   if (latestData) {
//     renderGameLayer(latestData)
//   }
// })

const renderGameLayer = (game) => {
  mapDom.innerHTML = ''
  const styleElement = document.createElement('style')
  styleElement.setAttribute('type', 'text/css')
  styleElement.textContent = `
  .map {
    grid-template-columns: repeat(${game.width}, 1fr);
    grid-template-rows: repeat(${game.height}, 1fr);
    width: calc((${16 * zoom}px * ${game.width}) - 240px);
    height: calc((${16 * zoom}px * ${game.height}) - 240px);
  }
  `
  document.head.appendChild(styleElement)
  let x = 0
  let y = 0
  game.tiles.forEach(tile => {
    if (tile === 1) {
      mapDom.insertAdjacentHTML(
        'beforeend',
        `<div
          class="tile"
          style="
            grid-column-start: ${x + 1};
            grid-row-start: ${y + 1};
            background-image: url('/entities/DDNet/1/0');
            "
          ></div>`)
    }
    x++
    if (x >= game.width) {
      x = 0
      y++
    }
  })
}

fetch('/api/v1/game')
  .then(res => res.json())
  .then((data) => {
    console.log(data)
    // set zoom to cover screen width with map width
    // on initial load
    if (latestData == null) {
      zoom = (window.innerWidth / 16) / data.width
    }
    latestData = data
    renderGameLayer(data)
  })
