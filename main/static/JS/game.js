const player = JSON.parse(document.getElementById('player').textContent);
let gameState = ["", "", "", "", "", "", "", "", ""]
let turn = player
const gameName = JSON.parse(document.getElementById('game-name').textContent);
const checkForWinner = (player) => {
  const combo = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]];
  for (let i = 0; i < combo.length; i++) {
    if (gameState[combo[i][0]] === player && gameState[combo[i][1]] === player
      && gameState[combo[i][2]] === player) return true;
  }
  return false;
}


const gameSocket = new WebSocket(
  'wss://'
  + window.location.host
  + '/ws/game/'
  + gameName
  + '/'
);

const restart = () => {
  gameState = ["", "", "", "", "", "", "", "", ""]
  const cells = document.querySelectorAll('.square');
  for (let cell of cells) {
    cell.childNodes[0].classList.remove('x', 'o');
  }
}

gameSocket.onmessage = ev => {
  const data = JSON.parse(ev.data);
  console.log(data['message'])
  console.log(data['cell'])
  turn = data['turn']
  console.log(turn)
  let id = data['cell']
  console.log('id' + id)
  const swalWithBootstrapButtons = Swal.mixin({
      customClass: {
        confirmButton: 'btn btn-success',
        cancelButton: 'btn btn-danger'
      },
      buttonsStyling: false
    })
  if (data['message'] === 'won') {
    console.log('THIS IS THE MESSAGE OF WINNING >>> ' + player)

    if (player === turn) { // player won
      swalWithBootstrapButtons.fire({
        title: 'You won!',
        text: "Do you want to restart a game?(Your opponent needs to choose this option too)",
        icon: 'success',
        showCancelButton: true,
        confirmButtonText: 'Yes, restart it!',
        cancelButtonText: 'No, cancel!',
        reverseButtons: true
      }).then((result) => {
        if (result.isConfirmed) {
          restart()
          swalWithBootstrapButtons.fire(
            'Restated!',
            'Game has been restarted.',
            'success'
          )
        } else if (
          /* Read more about handling dismissals below */
          result.dismiss === Swal.DismissReason.cancel
        ) {
          swalWithBootstrapButtons.fire(
            'Cancelled',
            'You will be redirected to the main page :)',
            'error'
          )
          window.location.replace(window.hostname);
        }
      })

    } else { // player lost
      swalWithBootstrapButtons.fire({
        title: 'You lost!',
        text: "Do you want to restart a game?(Your opponent needs to choose this option too)",
        icon: 'error',
        showCancelButton: true,
        confirmButtonText: 'Yes, restart it!',
        cancelButtonText: 'No, cancel!',
        reverseButtons: true
      }).then((result) => {
        if (result.isConfirmed) {
          restart();
          swalWithBootstrapButtons.fire(
            'Restated!',
            'Game has been restarted.',
            'success'
          )
        } else if (result.dismiss === Swal.DismissReason.cancel) {
          swalWithBootstrapButtons.fire(
            'Cancelled',
            'You will be redirected to the main page :)',
            'error'
          )
          window.location.replace(window.hostname);
        }
      })
    }
    } else if (data['message'] === 'game_is_over') {
      swalWithBootstrapButtons.fire({
        title: 'Tie!',
        text: "Do you want to restart a game?(Your opponent needs to choose this option too)",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, restart it!',
        cancelButtonText: 'No, cancel!',
        reverseButtons: true
      }).then((result) => {
        if (result.isConfirmed) {
          restart();
          swalWithBootstrapButtons.fire(
            'Restated!',
            'Game has been restarted.',
            'success'
          )
        } else if (
          /* Read more about handling dismissals below */
          result.dismiss === Swal.DismissReason.cancel
        ) {
          swalWithBootstrapButtons.fire(
            'Cancelled',
            'You will be redireced to the main page :)',
            'error'
          )
          window.location.replace(window.hostname);
        }
      })

  }

  const cell = document.getElementById(id)
  if (cell.childNodes[0].classList.length === 0) {
    cell.childNodes[0].classList.add(turn)
    gameState[cell.id] = turn
  }
  turn = turn === 'x' ? 'o' : 'x';
}

gameSocket.onclose = ev => {
  console.error('Chat socket closed unexpectedly');
};


const cells = document.querySelectorAll('.square');
console.log(cells)
for (let cell of cells) {
  cell.addEventListener('click', () => {
    if (cell.childNodes[0].classList.length === 0 && player === turn) {
      cell.childNodes[0].classList.add(turn);
      gameState[cell.id] = player;
      let message = ''
      if (checkForWinner(player)) {
        console.log(player + " won!");
        message = 'won'
      } else if (gameState.find(el => el === "") === undefined) {
        message = 'game_is_over'
      }
      gameSocket.send(JSON.stringify({
        'message': message,
        'cell': cell.id,
        'turn': turn,
      }))
    }
  })
}