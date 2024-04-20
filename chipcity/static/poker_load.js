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
    socket.onopen = function(event) {
        displayMessage("WebSocket Connected")
    }

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
    console.log("made it to display cards")
        // clear the board first 
        for (let i = 1; i <= 6; i++) {
            let curr_pfp = document.getElementById(`pfp${i}`)
            curr_pfp.src = ''
            let curr_hand_left = document.getElementById(`player${i}_left_front`)
            curr_hand_left.src = ""
            let curr_hand_right = document.getElementById(`player${i}_right_front`)
            curr_hand_right.src = ""

            curr_hand_left.style.width = 0
            curr_hand_left.style.height = 0

            curr_hand_right.style.width = 0
            curr_hand_right.style.height = 0
        }

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
            let player_left = document.getElementById("player1_left_front")
            let player_left_back = document.getElementById("player1_left_back")
            let player_right = document.getElementById("player1_right_front")
            let player_right_back = document.getElementById("player1_right_back")
            
            player_left.style.width = "59px";
            player_left.style.height = "100px";
            player_left.style.marginLeft = "-5px"
            player_left.style.marginTop = "-8px"

            player_left_back.style.width = "59px";
            player_left_back.style.height = "100px";
            player_left_back.style.marginLeft = "-5px"
            player_left_back.style.marginTop = "-8px"

            player_right.style.width = "59px";
            player_right.style.height = "100px";
            player_right.style.marginLeft = "-5px"
            player_right.style.marginTop = "-8px"

            player_right_back.style.width = "59px";
            player_right_back.style.height = "100px";
            player_right_back.style.marginLeft = "-5px"
            player_right_back.style.marginTop = "-8px"


            let player_left_id = player['card_left']
            let player_right_id = player['card_right']
            let player_left_file = cards[player_left_id]
            let player_right_file = cards[player_right_id]
            player_left.src = folder + player_left_file
            player_right.src = folder + player_right_file


            // display the pfp
            let player_pfp = document.getElementById("pfp1")
            let player_pfp_link = player['picture']
            player_pfp.src = player_pfp_link


            let file = cards["not-folded-back-art"]
            let source = folder + file
            player_left_back.src = source 
            player_right_back.src = source

    
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
            let player_left = document.getElementById(`player${seat_index}_left_front`)
            let player_right = document.getElementById(`player${seat_index}_right_front`)
            let file_left_id = player['card_left']
            // console.log(file_left)
            let file_right_id = player['card_right']
            // console.log(file_right)
            let file_left = cards[file_left_id]
            let file_right = cards[file_right_id]
            player_left.src = folder + file_left
            player_right.src = folder + file_right
            let player_pfp = document.getElementById(`pfp${seat_index}`)
            let player_pfp_link = player['picture']
            player_pfp.style.backgroundImage = `url(${player_pfp_link})`
            player_pfp.src = player_pfp_link

            player_left.style.width = "59px";
            player_left.style.height = "100px";
            player_left.style.marginLeft = "-5px"
            player_left.style.marginTop = "-8px"

            player_right.style.width = "59px";
            player_right.style.height = "100px";
            player_right.style.marginLeft = "-5px"
            player_right.style.marginTop = "-8px"
        }

    }
    }


    // this is the part where we display the middle cards
// Set image sources and adjust styles
    let left_flop_front = document.getElementById("left-flop_front");
    let left_flop_back = document.getElementById("left-flop_back");
    let middle_flop_front = document.getElementById("middle-flop_front");
    let middle_flop_back = document.getElementById("middle-flop_back");
    let right_flop_front = document.getElementById("right-flop_front");
    let right_flop_back = document.getElementById("right-flop_back");
    let turn_front = document.getElementById("turn_front"); 
    let turn_back = document.getElementById("turn_back"); 
    let river_front = document.getElementById("river_front"); 
    let river_back = document.getElementById("river_back"); 


    left_flop_front.style.width = "79px";
    left_flop_front.style.height = "120px";
    left_flop_front.style.marginLeft = "-4.5px"
    left_flop_front.style.marginTop = "-3.5px"
    left_flop_back.style.width = "79px";
    left_flop_back.style.height = "120px";
    left_flop_back.style.marginLeft = "-6.5px"
    left_flop_back.style.marginTop = "-3.5px"

    middle_flop_front.style.width = "79px";
    middle_flop_front.style.height = "120px";
    middle_flop_front.style.marginLeft = "-4.5px"
    middle_flop_front.style.marginTop = "-3.5px"
    middle_flop_back.style.width = "79px";
    middle_flop_back.style.height = "120px";
    middle_flop_back.style.marginLeft = "-6.5px"
    middle_flop_back.style.marginTop = "-3.5px"

    right_flop_front.style.width = "79px";
    right_flop_front.style.height = "120px";
    right_flop_front.style.marginLeft = "-4.5px"
    right_flop_front.style.marginTop = "-3.5px"
    right_flop_back.style.width = "79px";
    right_flop_back.style.height = "120px";
    right_flop_back.style.marginLeft = "-6.5px"
    right_flop_back.style.marginTop = "-3.5px"

    turn_front.style.width = "79px";
    turn_front.style.height = "120px";
    turn_front.style.marginLeft = "-4.5px"
    turn_front.style.marginTop = "-3.5px"
    turn_back.style.width = "79px";
    turn_back.style.height = "120px";
    turn_back.style.marginLeft = "-6.5px"
    turn_back.style.marginTop = "-3.5px"

    river_front.style.width = "79px";
    river_front.style.height = "120px";
    river_front.style.marginLeft = "-4.5px"
    river_front.style.marginTop = "-3.5px"
    river_back.style.width = "79px";
    river_back.style.height = "120px";
    river_back.style.marginLeft = "-6.5px"
    river_back.style.marginTop = "-3.5px"

    // Display cards based on game state
    if (game_info['curr_round'] == 0) {
        // display all red cards
        let file = cards["not-folded-back-art"];
        let source = folder + file;
        left_flop_back.src = source;
        middle_flop_back.src = source;
        right_flop_back.src = source;
        turn_back.src = source; 
        river_back.src = source; 

    } else if (game_info['curr_round'] == 1) {
        let left_flop_id = game_info['flop1'];
        let left_file = cards[left_flop_id];
        left_flop_front.src = folder + left_file;
        left_flop_front.parentElement.parentElement.classList.add('flip');

        let middle_flop_id = game_info['flop2'];
        let middle_file = cards[middle_flop_id];
        middle_flop_front.src = folder + middle_file;
        middle_flop_front.parentElement.parentElement.classList.add('flip');

        let right_flop_id = game_info['flop3'];
        let right_file = cards[right_flop_id];
        right_flop_front.src = folder + right_file;
        right_flop_front.parentElement.parentElement.classList.add('flip');
        


    }
        //           <div class="right-flop_container" id="cardContainer">
        //     <div class="card">
        //       <div class="flipper">
        //         <div class="front">
        //           <img id = "right-flop_front"/>
        //         </div>
        //         <div class="back">
        //           <img id = "right-flop_back"/>             
        //          </div>
        //     </div>
        //   </div>          



    if (game_info['curr_round'] == 2 || game_info['curr_round'] >= 4){
        let turn_front = document.getElementById("turn_front"); 
        let turn_id = game_info['turn'];
        let turn_file = cards[turn_id];
        turn_front.src = folder + turn_file;
        turn_front.parentElement.parentElement.classList.add('flip');

    }
    if (game_info['curr_round'] == 3 || game_info['curr_round'] >= 4){
        let river_front = document.getElementById("river_front"); 
        let river_id = game_info['river'];
        let river_file = cards[river_id];
        river_front.src = folder + river_file;
        river_front.parentElement.parentElement.classList.add('flip');

    }
    if (game_info['curr_round'] >= 4){
        // flip over all the active hand cards
        displayPlaceholderButtons(game_info)
        for (let player_id in players){
            // console.log(player_id)
            let player = players[player_id]
            if (player.user == myUserName){
                // display the current user
                let player_left = document.getElementById("player1_left_front")
                let player_left_back = document.getElementById("player1_left_back")
                let player_right = document.getElementById("player1_right_front")
                let player_right_back = document.getElementById("player1_right_back")

                let player_left_id = player['card_left']
                let player_right_id = player['card_right']
                let player_left_file = cards[player_left_id]
                let player_right_file = cards[player_right_id]
                player_left.src = folder + player_left_file
                player_right.src = folder + player_right_file
                let file = cards["not-folded-back-art"]
                let source = folder + file
                player_left_back.src = source 
                player_right_back.src = source

                player_left.style.width = "59px";
                player_left.style.height = "100px";
                player_left.style.marginLeft = "-5px"
                player_left.style.marginTop = "-8px"

                player_left_back.style.width = "59px";
                player_left_back.style.height = "100px";
                player_left_back.style.marginLeft = "-5px"
                player_left_back.style.marginTop = "-8px"

                player_right.style.width = "59px";
                player_right.style.height = "100px";
                player_right.style.marginLeft = "-5px"
                player_right.style.marginTop = "-8px"

                player_right_back.style.width = "59px";
                player_right_back.style.height = "100px";
                player_right_back.style.marginLeft = "-5px"
                player_right_back.style.marginTop = "-8px"
        
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
                }
                let player_left = document.getElementById(`player${seat_index}_left_front`)
                let player_right = document.getElementById(`player${seat_index}_right_front`)
                let file_left_id = player['card_left']
                // console.log(file_left)
                let file_right_id = player['card_right']
                // console.log(file_right)
                let file_left = cards[file_left_id]
                let file_right = cards[file_right_id]
                player_left.src = folder + file_left
                player_right.src = folder + file_right
                
                player_left.style.width = "59px";
                player_left.style.height = "100px";
                player_left.style.marginLeft = "-5px"
                player_left.style.marginTop = "-8px"

                player_right.style.width = "59px";
                player_right.style.height = "100px";
                player_right.style.marginLeft = "-5px"
                player_right.style.marginTop = "-8px"
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
    let data = {gameState: "ready", text: "", user_pressed_ready: myUserName}
    socket.send(JSON.stringify(data))
}

// }
function callAction(){
    let data = {user: myUserName, gameState: "inProgress", player_action: "call", text:""}
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

