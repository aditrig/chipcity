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
        let game
        let a_players
        let n_players
        if (game_info.length > 0){
            game = game_info[0]
        } else{
            game = null
        }
        if (active_players_info.length > 0){
            a_players = active_players_info[0]
        } else{
            a_players = null
        }
        if (non_active_players_info.length > 0){
            n_players = active_players_info[0]
        } else{
            n_players = null
        }
        processMessage(game, a_players, n_players)
        // console.log('Game Info', JSON.parse(response.game_info));
        // console.log('Active Players', JSON.parse(response.active_players_info));
        // console.log('Non Active Players', JSON.parse(response.non_active_players_info))

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

function processMessage(game_info, active_players_info, non_active_players_info){
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
    }
    else{
        console.log("game info is null")
    }

}


function displayActiveButtons(game_info){
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
}


function startGame() {

    let data = {gameState: "ready", text: ""}
    socket.send(JSON.stringify(data))
}

// function startPlay(){
//     let data = {gameState: "inProgress", text: ""}
//     socket.send(JSON.stringify(data))

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