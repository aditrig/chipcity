"use strict"

/*
 * Use a global variable for the socket.  Poor programming style, I know,
 * but I think the simpler implementations of the deleteItem() and addItem()
 * functions will be more approachable for students with less JS experience.
 */
let socket = null


function connectToServer() {
    // Use wss: protocol if site using https:, otherwise use ws: protocol
    let wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:"

    // Create a new WebSocket.
    let url = `${wsProtocol}//${window.location.host}/table/data`

    socket = new WebSocket(url)


    // Handle any errors that occur.
    socket.onerror = function(error) {
        displayMessage("WebSocket Error: " + error)
    }

    // Show a connected message when the WebSocket is opened.
    // socket.onopen = function(event) {
    //     displayMessage("WebSocket Connected")
    // }

    // Show a disconnected message when the WebSocket is closed.
    socket.onclose = function(event) {
        displayMessage("WebSocket Disconnected")
    }

    // Handle messages received from the server.
    socket.onmessage = function(event) {
        console.log("hi")
        // so here we have our response from the server and we want to utilize it to 
        let response = JSON.parse(event.data)
        console.log(response)
        console.log(response.game_info)
        let game_info = JSON.parse(response.game_info)
        let active_players_info = JSON.parse(response.active_players_info)
        let non_active_players_info = JSON.parse(response.non_active_players_info)
        let cards_info = JSON.parse(response.cards)
        let game
        let a_players
        let n_players
        let cards
        console.log('Game Info', JSON.parse(response.game_info));
        console.log('Active Players', JSON.parse(response.active_players_info));
        console.log('Non Active Players', JSON.parse(response.non_active_players_info))
        console.log(cards_info)
        if (game_info.length > 0){
            game = game_info[(game_info.length)-1]
        } else{
            game = null
        }
        if (active_players_info.length > 0){
            a_players = active_players_info[(active_players_info.length)-1]
        } else{
            a_players = null
        }
        if (non_active_players_info.length > 0){
            n_players = non_active_players_info[(non_active_players_info.length) -1]
        } else{
            n_players = null
        }
        if (cards_info.length > 0){
            cards = cards_info[cards_info.length-1]
        } else{
            cards = null
        }
        processMessage(game, cards, active_players_info, n_players)

        // socket.onmessage = function(event) {
        //     let response = JSON.parse(event.data)
        //     if (Array.isArray(response)) {
        //         updateList(response)
        //     } else {
        //         displayResponse(response)
        //     }
        // }

        
    }
}

function displayError(message) {
    let errorElement = document.getElementById("testing")
    errorElement.innerHTML = message}

function displayMessage(message) {
    let errorElement = document.getElementById("testing")
    errorElement.innerHTML = message
}

function displayResponse(response) {
    if ("error" in response) {
        displayError(response.error)
    } else if ("message" in response) {
        displayMessage(response.message)
    } else {
        displayMessage("Unknown response")
    }
}

function processMessage(game_info, cards, active_players_info, non_active_players_info){
    // check if the current player is the user
    // if it is, display buttons
    console.log("makes it to processMessage, check if user is currentPlayer")
    if (game_info != null){
        console.log("game info is not null")
        if (game_info["current_player_user"] == myUserName){
            console.log("display Active Buttons")
    
            displayActiveButtons(game_info)
        }
        else{
            console.log("don't display active buttons")
    
            displayPlaceholderButtons(game_info)
        }
        displayCards(game_info, cards, active_players_info)
    }
    else{
        console.log("game info is null")
    }

}

function displayCards(game_info, cards, players){
    console.log("made it to display cards")
    // display the players cards based on who the player is
    // make a for loop for the players and if the player is the user than 
    // display the cards, if not then don't???
    let folder = "../static/img/cards/"
    // let count = 1
    console.log("this is the players")
    console.log(players)
    // console.log(game_info['list_of_active_players'])
    // services = "['service1', 'service2', 'service3']"
    // services = services.replace(/'/g, '"') //replacing all ' with "
    // services = JSON.parse(services)
    // console.log(services)
    let list_of_players = game_info['list_of_active_players']
    list_of_players = list_of_players.replace(/'/g, '"')
    list_of_players = JSON.parse(list_of_players)
    console.log(list_of_players)
    console.log(typeof list_of_players)
    let logged_in_user_index = list_of_players.indexOf(myUserName)
    console.log("this is my user name")
    console.log(myUserName)
    console.log("this is the logged in user index")
    console.log(logged_in_user_index)
    if (game_info["curr_round"] < 4){
    for (let player_id in players){
        // console.log(player_id)
        let player = players[player_id]
        if (player.user == myUserName){
            // display the current user
            let player_left = document.getElementById("player1_left")
            let player_right = document.getElementById("player1_right")
            let player_left_id = player['card_left']
            let player_right_id = player['card_right']
            let player_left_file = cards[player_left_id]
            let player_right_file = cards[player_right_id]
            player_left.src = folder + player_left_file
            player_right.src = folder + player_right_file
    
        } else{
            let curr_user_index = list_of_players.indexOf(player.user)
            console.log("this is the current user index")
            console.log(curr_user_index)
            let distance = Math.abs(curr_user_index - logged_in_user_index)
            console.log("this is the calculated distance")
            console.log(distance)
            // if the curr user index < logged_in_user_index, curr user on the right
            let seat_index
            if (curr_user_index < logged_in_user_index){
                console.log("the user shoudl be on the right of the logged in")
                // curr user on the right of the logged in user
                seat_index = 1 + distance
                console.log("this is the seat number")
                console.log(seat_index)
                // display to the right
                
            }
            // if logged_in_user_index < curr user index, curr user on the left
            else if (logged_in_user_index < curr_user_index){
                seat_index = 7 - distance
                console.log("this is the seat number")
                console.log(seat_index)
                // display to the right
                // let player_left = document.getElementById(`player${seat_index}_left`)
                // let player_right = document.getElementById(`player${seat_index}_right`)
                // let file = cards["not-folded-back-art"]
                // let source = folder + file
                // player_left.src = source
                // player_right.src = source
            } 
            // let player_left = document.getElementById(`player${seat_index}_left`)
            // let player_right = document.getElementById(`player${seat_index}_right`)
            // let file = cards["not-folded-back-art"]
            // let source = folder + file
            // player_left.src = source
            // player_right.src = source
            let player_left = document.getElementById(`player${seat_index}_left`)
            let player_right = document.getElementById(`player${seat_index}_right`)
            let file_left = player['card_left']
            let file_right = player['card_right']
            player_left.src = folder + file_left
            player_right.src = folder + file_right


        }

    }
    }


    // this is the part where we display the middle cards
    let left_flop = document.getElementById("left-flop")
    let right_flop = document.getElementById("right-flop")
    let middle_flop = document.getElementById("middle-flop")
    let turn = document.getElementById("turn")
    let river = document.getElementById("river")

    left_flop.style.width = "65px"
    left_flop.style.height = "108px"
    right_flop.style.width = "65px"
    right_flop.style.height = "108px"
    middle_flop.style.width = "65px"
    middle_flop.style.height = "108px"
    turn.style.width = "65px"
    turn.style.height = "108px"
    river.style.width = "65px"
    river.style.height = "108px"

    if (game_info['curr_round'] == 0){
        // display all red cards
        let file = cards["not-folded-back-art"]
        let source = folder + file
        left_flop.src = source
        right_flop.src = source
        middle_flop.src = source
        turn.src = source
        river.src = source
    }
    if (game_info['curr_round'] == 1){
        let left_flop_id = game_info['flop1']
        let left_file = cards[left_flop_id]
        left_flop.src = folder + left_file
        let middle_flop_id = game_info['flop2']
        let middle_file = cards[middle_flop_id]
        middle_flop.src = folder + middle_file
        let right_flop_id = game_info['flop3']
        let right_file = cards[right_flop_id]
        right_flop.src = folder + right_file
    }
    if (game_info['curr_round'] == 2){
        let turn_id = game_info['turn']
        console.log(game_info['turn'])
        let turn_file = cards[turn_id]
        console.log(turn_file)
        console.log(folder+turn_file)
        turn.src = folder + turn_file
    }
    if (game_info['curr_round'] == 3){
        let river_id = game_info['river']
        let river_file = cards[river_id]
        river.src = folder + river_file
    }
    if (game_info['curr_round'] >= 4){
        // flip over all the active hand cards
        for (let player_id in players){
            // console.log(player_id)
            let player = players[player_id]
            if (player.user == myUserName){
                // display the current user
                let player_left = document.getElementById("player1_left")
                let player_right = document.getElementById("player1_right")
                let player_left_id = player['card_left']
                let player_right_id = player['card_right']
                let player_left_file = cards[player_left_id]
                let player_right_file = cards[player_right_id]
                player_left.src = folder + player_left_file
                player_right.src = folder + player_right_file
        
            } else{
                let curr_user_index = list_of_players.indexOf(player.user)
                console.log("this is the current user index")
                console.log(curr_user_index)
                let distance = Math.abs(curr_user_index - logged_in_user_index)
                console.log("this is the calculated distance")
                console.log(distance)
                // if the curr user index < logged_in_user_index, curr user on the right
                let seat_index
                if (curr_user_index < logged_in_user_index){
                    console.log("the user shoudl be on the right of the logged in")
                    // curr user on the right of the logged in user
                    seat_index = 1 + distance
                    console.log("this is the seat number")
                    console.log(seat_index)
                    // display to the right
                    
                }
                // if logged_in_user_index < curr user index, curr user on the left
                else if (logged_in_user_index < curr_user_index){
                    seat_index = 7 - distance
                    console.log("this is the seat number")
                    console.log(seat_index)
                    // display to the right
                    // let player_left = document.getElementById(`player${seat_index}_left`)
                    // let player_right = document.getElementById(`player${seat_index}_right`)
                    // let file2_left = player['card_left']
                    // let file2_right = player['card_right']
                    // player_left.src = folder + file2_left
                    // player_right.src = folder + file2_right
                } 
                let player_left = document.getElementById(`player${seat_index}_left`)
                let player_right = document.getElementById(`player${seat_index}_right`)
                let file_left = player['card_left']
                let file_right = player['card_right']
                player_left.src = folder + file_left
                player_right.src = folder + file_right
    
    
            }
    }

}
}

function inc(chips){
    var value = parseInt(document.getElementById('raiseAmount').value ,10) 
    value = isNaN(value) ? 0 : value;
    value++;
    document.getElementById('number').value = value;

}

function dec(chips){
    if (chips > 0) {
        var value = parseInt(document.getElementById('raiseAmount').value ,10) 
        value = isNaN(value) ? 0 : value;
        value--;
        document.getElementById('number').value = value;
        }
}


function displayActiveButtons(game_info){
    var chips = 0

    let callDisplay
    callDisplay = document.getElementById("callButton")
    callDisplay.style.visibility = 'visible'
    callDisplay.onclick = function (){callAction()}
    let raiseDisplay
    raiseDisplay = document.getElementById("raiseButton")
    raiseDisplay.style.visibility = 'visible'
    raiseDisplay.onclick = function (){raiseAction()}
    let raiseForm
    raiseForm = document.getElementById("raiseForm")
    raiseForm.style.visibility = 'visible'
    let raiseAmount
    raiseAmount = document.getElementById("raiseAmount")
    raiseAmount.style.visibility = 'visible'
    let foldDisplay
    foldDisplay = document.getElementById("foldButton")
    foldDisplay.style.visibility = 'visible'
    foldDisplay.onclick = function (){foldAction()}
    let checkDisplay
    checkDisplay = document.getElementById("checkButton")
    checkDisplay.style.visibility = 'visible'
    checkDisplay.onclick = function (){checkAction()}
    let incrementButton
    let decrementButton
    incrementButton = document.getElementById("addRaise")
    incrementButton.style.visibility = 'visible'
    incrementButton.onclick = function (){inc(chips)}
    decrementButton = document.getElementById("subtractRaise") 
    decrementButton.style.visibility = 'visible'
    decrementButton.onclick = function (){dec(chips)}

}

function displayPlaceholderButtons(game_info){
    let callDisplay
    callDisplay = document.getElementById("callButton")
    callDisplay.style.visibility = 'hidden'
    callDisplay.onclick = function(){}
    let raiseDisplay
    raiseDisplay = document.getElementById("raiseButton")
    raiseDisplay.style.visibility = 'hidden'
    raiseDisplay.onclick = function(){}
    let raiseForm
    raiseForm = document.getElementById("raiseForm")
    raiseForm.style.visibility = 'hidden'
    let raiseAmount
    raiseAmount = document.getElementById("raiseAmount")
    raiseAmount.style.visibility = 'hidden'
    let checkDisplay
    checkDisplay = document.getElementById("checkButton")
    checkDisplay.style.visibility = 'hidden'
    checkDisplay.onclick = function(){}
    let foldDisplay
    foldDisplay = document.getElementById("foldButton")
    foldDisplay.style.visibility = 'hidden'
    foldDisplay.onclick = function(){}
    let incrementButton
    let decrementButton
    incrementButton = document.getElementById("addRaise")
    incrementButton.style.visibility =  'hidden'
    incrementButton.onclick =function(){}
    decrementButton = document.getElementById("subtractRaise") 
    decrementButton.style.visibility = 'hidden'
    decrementButton.onclick = function(){}

}


function startGame() {

    let data = {gameState: "ready", text: ""}
    socket.send(JSON.stringify(data))
}

// }
function callAction(){
    let data = {user: myUserName, gameState: "inProgress", player_action: "call" , text:""}
    socket.send(JSON.stringify(data))
}
function raiseAction(){
    let data = {user: myUserName, gameState: "inProgress", player_action: "raise," + document.getElementById('raiseAmount').value, text:""}
    socket.send(JSON.stringify(data))
}
function checkAction(){
    let data = {user: myUserName, gameState: "inProgress", player_action: "check", text:""}
    socket.send(JSON.stringify(data))
}
function foldAction(){
    let data = {user: myUserName, gameState: "inProgress", player_action: "fold", text:""}
    socket.send(JSON.stringify(data))
}



// function updateList(items) {
//     // Removes items from todolist if they not in items
//     let liElements = document.getElementsByTagName("li")
//     for (let i = 0; i < liElements.length; i++) {
//         let element = liElements[i]
//         let deleteIt = true
//         items.forEach(item => {
//             if (element.id === `id_item_${item.id}`) deleteIt = false
//         })
//         if (deleteIt) element.remove()
//     }

//     // Adds each to do list item received from the server to the displayed list
//     let list = document.getElementById("todo-list")
//     items.forEach(item => {
//         if (document.getElementById(`id_item_${item.id}`) == null) {
//             list.append(makeListItemElement(item))
//         }
//     })
// }

// // Builds a new HTML "li" element for the to do list
// function makeListItemElement(item) {
//     let deleteButton
//     if (item.user === myUserName) {
//         deleteButton = `<button onclick='deleteItem(${item.id})'>X</button>`
//     } else {
//         deleteButton = "<button style='visibility: hidden'>X</button> "
//     }

//     let details = `<span class="details">(id=${item.id}, ip_addr=${item.ip_addr}, user=${item.user})</span>`

//     let element = document.createElement("li")
//     element.id = `id_item_${item.id}`
//     element.innerHTML = `${deleteButton} ${sanitize(item.text)} ${details}`

//     return element
// }

// function sanitize(s) {
//     // Be sure to replace ampersand first
//     return s.replace(/&/g, '&amp;')
//             .replace(/</g, '&lt;')
//             .replace(/>/g, '&gt;')
//             .replace(/"/g, '&quot;')
// }

// function addItem() {
//     let textInputEl = document.getElementById("item")
//     let itemText = textInputEl.value
//     if (itemText === "") return

//     // Clear previous error message, if any
//     displayError("")
    
//     let data = {action: "add", text: itemText}
//     socket.send(JSON.stringify(data))

//     textInputEl.value = ""
// }

// function deleteItem(id) {
//     let data = {action: "delete", id: id}
//     socket.send(JSON.stringify(data))
// }

// // def join_table():
// //     document.getElementById('id_join_table').addEventListener('click', function() {
// //         window.location.href = '{%url 'table' %}}';
// //     })
