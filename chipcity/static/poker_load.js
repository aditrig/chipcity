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
            // no games exist to show the readybutton
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
        displayGameInfo(game, active_players_info)

        
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
        let readyDisplay
        readyDisplay = document.getElementById("start-button")

        if (game_info["curr_round"]<5){
            readyDisplay.style.visibility = 'hidden'
            readyDisplay.onclick = function(){}
        }
        if (game_info["curr_round"]==5){
            readyDisplay.style.visibility = 'visible'
            readyDisplay.onclick = function(){startGame()}

        }
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
        displayHighlight(game_info, active_players_info)
    }
    else{
        console.log("game info is null")
    }

}

function displayGameInfo(game_info, players){
    // display the total pot
    let pot_text = document.getElementById("id_total_pot")
    pot_text.textContent = `${game_info['total_pot']}`

    let tp = document.getElementById("TPCHIPS")
    tp.style.fontSize = "20px"
    tp.innerHTML = "CHIPS"

    // display the username for each player
    // display the current bet for each player
    // display the total chips for each player
    let list_of_players = game_info['list_of_active_players']
    list_of_players = list_of_players.replace(/'/g, '"')
    list_of_players = JSON.parse(list_of_players)
    let logged_in_user_index = list_of_players.indexOf(myUserName)
    for (let player_id in players){
        let player = players[player_id]
        if (player.user == myUserName){
            console.log("displaying the username")
            // display as user 1
            let user_1 = document.getElementById("id_user_1")
            user_1.textContent = `${player.user}`
            user_1.style.top = "0%"
            user_1.style.left = "0%"
            user_1.style.position = "absolute"

            let user_chips = document.getElementById("id_total_chips_1")
            user_chips.textContent = `${player['chips']}`

            let tc_1 = document.getElementById("TCCHIPS1")
            tc_1.style.fontSize = "10px"
            tc_1.innerHTML = "CHIPS"
            tc_1.style.opacity = "100%"

            let tcg_div = document.getElementById("user_total_chips_group_1")
            tcg_div.style.borderRadius = "20px"
            tcg_div.style.border = "1px solid #EEDBC0"
            tcg_div.style.background = "#DFC7A7"
            tcg_div.style.boxShadow = "0px 4px 4px 0px rgba(0, 0, 0, 0.25)"
            tcg_div.style.opacity = "100%"

            let user_bet = document.getElementById("id_current_bet_1")
            user_bet.textContent = `${player['current_bet']}`
            user_bet.style.position = "relative"
            user_bet.style.top = "-3px"

            let chips_1 = document.getElementById("CHIPS1")
            chips_1.style.fontSize = "10px"
            chips_1.innerHTML = "CHIPS"
            chips_1.style.position = "relative"
            chips_1.style.top = "-3px"
            

            let group_bet_div = document.getElementById("current_bet_group_1")
            group_bet_div.style.width = "68px"
            group_bet_div.style.height = "23px"
            group_bet_div.style.flexShrink = "0"
            group_bet_div.style.borderRadius = "20px"
            group_bet_div.style.border = "1px solid #DA92D0"
            group_bet_div.style.background = "#BE7EB5"
            group_bet_div.style.boxShadow = "0px 4px 4px 0px rgba(0, 0, 0, 0.25)"
        }
        else{
            let curr_user_index = list_of_players.indexOf(player.user)
            let distance = Math.abs(curr_user_index - logged_in_user_index)
            let seat_index
            if (curr_user_index < logged_in_user_index){
                // curr user on the right of the logged in user
                seat_index = 1 + distance
            }
            // if logged_in_user_index < curr user index, curr user on the left
            else if (logged_in_user_index < curr_user_index){
                seat_index = 7 - distance
            }
            let user = document.getElementById(`id_user_${seat_index}`)
            user.textContent = `${player.user}`
            user.style.top = "0%"
            user.style.left = "0%"
            user.style.position = "absolute"

            let user_chips = document.getElementById(`id_total_chips_${seat_index}`)
            user_chips.textContent = `${player['chips']}`

            let tc = document.getElementById(`TCCHIPS${seat_index}`)
            tc.style.fontSize = "10px"
            tc.innerHTML = "CHIPS"
            tc.style.opacity = "100%"

            let tcg_div = document.getElementById(`user_total_chips_group_${seat_index}`)
            tcg_div.style.borderRadius = "20px"
            tcg_div.style.border = "1px solid #EEDBC0"
            tcg_div.style.background = "#DFC7A7"
            tcg_div.style.boxShadow = "0px 4px 4px 0px rgba(0, 0, 0, 0.25)"
            tcg_div.style.opacity = "100%"

            let user_bet = document.getElementById(`id_current_bet_${seat_index}`)
            user_bet.textContent = `${player['current_bet']}`
            user_bet.style.position = "relative"
            user_bet.style.top = "-3px"

            let chips = document.getElementById(`CHIPS${seat_index}`)
            chips.style.fontSize = "10px"
            chips.innerHTML = "CHIPS"
            chips.style.position = "relative"
            chips.style.top = "-3px"

            let group_bet_div = document.getElementById(`current_bet_group_${seat_index}`)
            group_bet_div.style.width = "68px"
            group_bet_div.style.height = "23px"
            group_bet_div.style.flexShrink = "0"
            group_bet_div.style.borderRadius = "20px"
            group_bet_div.style.border = "1px solid #DA92D0"
            group_bet_div.style.background = "#BE7EB5"
            group_bet_div.style.boxShadow = "0px 4px 4px 0px rgba(0, 0, 0, 0.25)"
        }
        
        let turn_indicator = document.getElementById('logo');
        let current_turn_user = game_info['current_player_user'];
        if (current_turn_user && current_turn_user === myUserName) {
            turn_indicator.textContent = "It's your turn!";
        } else {
            // Reset to default text if it's not the user's turn
            turn_indicator.textContent = `${current_turn_user} is taking their turn`;

        }
        if (game_info['curr_round'] == 5) {
            displayGameOver(game_info)
        }
    
    }

}


function displayCards(game_info, cards, players){
    console.log("made it to display cards")
        // clear the board first 
    
        for (let i = 1; i <= 6; i++) {
            let user_tc_group = document.getElementById(`user_total_chips_group_${i}`)
            user_tc_group.style.background = "none"
            user_tc_group.style.border = "0px"
            user_tc_group.style.boxShadow = "none"

            let id_user = document.getElementById(`id_user_${i}`)
            id_user.innerHTML = ""

            let user_tc = document.getElementById(`user_total_chips_group_${i}`)
            user_tc.style.opacity = "0"

            let TCCHIPS = document.getElementById(`TCCHIPS${i}`)
            TCCHIPS.style.opacity = "0"

            let user_bet = document.getElementById(`id_current_bet_${i}`)
            user_bet.innerHTML = ""

            let CHIPS = document.getElementById(`CHIPS${i}`)
            CHIPS.innerHTML = ""

            let user_chips_group = document.getElementById(`current_bet_group_${i}`)
            user_chips_group.style.background = "none"
            user_chips_group.style.border = "0px"
            user_chips_group.style.boxShadow = "none"

            let curr_pfp = document.getElementById(`pfp${i}_div`)
            curr_pfp.style.backgroundImage = "none"
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
    console.log("this is the players")
    console.log(players)
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
                let player_pfp = document.getElementById("pfp1_div")
                let player_pfp_link = player['picture']
                player_pfp.style.backgroundImage = `url(${player_pfp_link})`
                player_pfp.style.backgroundPosition = "center"
                player_pfp.src = player_pfp_link

                let folded = player['hand_is_active']
                let file
                if (!folded){
                    file = cards['folded-back-art']
                    
                } else{
                    file = cards["not-folded-back-art"]
                }
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
                }
                let player_left = document.getElementById(`player${seat_index}_left_back`)
                let player_right = document.getElementById(`player${seat_index}_right_back`)
                // let file_left_id = player['card_left']
                // let file_right_id = player['card_right']
                // let file_left = cards[file_left_id]
                // let file_right = cards[file_right_id]
                // let back = "not-folded-back-art.svg"
                // player_left.src = folder + back
                // player_right.src = folder + back
                let folded = player['hand_is_active']
                let file
                if (!folded){
                    file = cards['folded-back-art']
                    
                } else{
                    file = cards["not-folded-back-art"]
                }
                let source = folder + file
                player_left.src = source 
                player_right.src = source

                let player_pfp = document.getElementById(`pfp${seat_index}_div`)
                let player_pfp_link = player['picture']
                player_pfp.style.backgroundImage = `url(${player_pfp_link})`
                player_pfp.style.backgroundPosition = "center"
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

    let file = cards["not-folded-back-art"];
    let source = folder + file;
    left_flop_back.src = source;
    middle_flop_back.src = source;
    right_flop_back.src = source;
    turn_back.src = source; 
    river_back.src = source;
    let left_flop_id = game_info['flop1'];
    let left_file = cards[left_flop_id];
    left_flop_front.src = folder + left_file;
    let middle_flop_id = game_info['flop2'];
    let middle_file = cards[middle_flop_id];
    middle_flop_front.src = folder + middle_file;
    let right_flop_id = game_info['flop3'];
    let right_file = cards[right_flop_id];
    right_flop_front.src = folder + right_file;
    let turn_id = game_info['turn'];
    let turn_file = cards[turn_id];
    turn_front.src = folder + turn_file;
    let river_id = game_info['river'];
    let river_file = cards[river_id];
    river_front.src = folder + river_file;
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
    if ((game_info['curr_round'] == 0) && (game_info['game_num'] > 1)) {
        // display all red cards
        let file = cards["not-folded-back-art"];
        let source = folder + file;
        left_flop_back.src = source;
        middle_flop_back.src = source;
        right_flop_back.src = source;
        turn_back.src = source; 
        river_back.src = source;
        left_flop_front.parentElement.parentElement.classList.remove('flip-to-back');
        middle_flop_front.parentElement.parentElement.classList.remove('flip-to-back');
        right_flop_front.parentElement.parentElement.classList.remove('flip-to-back');
        turn_front.parentElement.parentElement.classList.remove('flip-to-back');
        river_front.parentElement.parentElement.classList.remove('flip-to-back')
        left_flop_front.parentElement.parentElement.classList.add('flip-to-front');
        middle_flop_front.parentElement.parentElement.classList.add('flip-to-front');
        right_flop_front.parentElement.parentElement.classList.add('flip-to-front');
        turn_front.parentElement.parentElement.classList.add('flip-to-front');
        river_front.parentElement.parentElement.classList.add('flip-to-front')

        var leftelement = document.querySelector('.lchp-1');
        var rightelement = document.querySelector('.rchp-1');

        leftelement.setAttribute('ontouchstart', "this.classList.toggle('hover');");
        rightelement.setAttribute('ontouchstart', "this.classList.toggle('hover');");

        let player_left = document.getElementById('player1_left_front')
        let player_right = document.getElementById('player1_right_front')

        player_left.parentElement.parentElement.classList.add('flip-to-front');
        player_right.parentElement.parentElement.classList.add('flip-to-front');
        player_left.parentElement.parentElement.classList.remove('flip-to-back');
        player_right.parentElement.parentElement.classList.remove('flip-to-back');

    } 
    if (game_info['curr_round'] == 1|| game_info['curr_round'] >= 4) {
        left_flop_front.parentElement.parentElement.classList.add('flip-to-back');
        left_flop_front.parentElement.parentElement.classList.remove('flip-to-front');
        middle_flop_front.parentElement.parentElement.classList.add('flip-to-back');
        middle_flop_front.parentElement.parentElement.classList.remove('flip-to-front');

        right_flop_front.parentElement.parentElement.classList.add('flip-to-back');
        right_flop_front.parentElement.parentElement.classList.remove('flip-to-front');

    }


    if (game_info['curr_round'] == 2 || game_info['curr_round'] >= 4){
        turn_front.parentElement.parentElement.classList.add('flip-to-back');
        turn_front.parentElement.parentElement.classList.remove('flip-to-front');
    }
    if (game_info['curr_round'] == 3 || game_info['curr_round'] >= 4){
        river_front.parentElement.parentElement.classList.add('flip-to-back');
        river_front.parentElement.parentElement.classList.remove('flip-to-front');

    }
    if (game_info['curr_round'] >= 4){
        // flip over all the active hand cards
        displayGameOver(game_info)
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

                var divElement = document.querySelector('.lchp-1');
                divElement.removeAttribute('ontouchstart');

                var divElement = document.querySelector('.rchp-1');
                divElement.removeAttribute('ontouchstart');

                let player_left_id = player['card_left']
                let player_right_id = player['card_right']
                let player_left_file = cards[player_left_id]
                let player_right_file = cards[player_right_id]
                

                player_left.parentElement.parentElement.classList.add('flip-to-back');
                player_left.parentElement.parentElement.classList.remove('flip-to-front');
                player_right.parentElement.parentElement.classList.add('flip-to-back');
                player_right.parentElement.parentElement.classList.remove('flip-to-front');

                
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

                // // flip it open
                // player_left.parentElement.parentElement.classList.add('flip-to-back');
                // player_left.parentElement.parentElement.classList.remove('flip-to-front');
                // player_right.parentElement.parentElement.classList.add('flip-to-back');
                // player_right.parentElement.parentElement.classList.remove('flip-to-front');

                let player_pfp = document.getElementById("pfp1_div")
                let player_pfp_link = player['picture']
                player_pfp.style.backgroundImage = `url(${player_pfp_link})`
                player_pfp.style.backgroundPosition = "center"
                player_pfp.src = player_pfp_link
        
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

                // flip it open
                player_left.parentElement.parentElement.classList.add('flip-to-back');
                player_left.parentElement.parentElement.classList.remove('flip-to-front');
                player_right.parentElement.parentElement.classList.add('flip-to-back');
                player_right.parentElement.parentElement.classList.remove('flip-to-front');

                let player_pfp = document.getElementById(`pfp${seat_index}_div`)
                let player_pfp_link = player['picture']
                player_pfp.style.backgroundImage = `url(${player_pfp_link})`
                player_pfp.style.backgroundPosition = "center"
                player_pfp.src = player_pfp_link
            }
        }
    }

}

function displayGameOver(game_info) {
    console.log(game_info['winning_player_user'])
    let winning_player = game_info['winning_player_user']
    let logo = document.getElementById('logo')
    logo.textContent = `${winning_player}`;
    logo.style.textTransform = "uppercase"
    logo.style.color = "#FFF"
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

function displayHighlight(game_info, players){
    let list_of_players = game_info['list_of_active_players']
    list_of_players = list_of_players.replace(/'/g, '"')
    list_of_players = JSON.parse(list_of_players)
    let logged_in_user_index = list_of_players.indexOf(myUserName)
    
    for (let player_id in players){
        let player = players[player_id]
        
            // find this player's location and display highlight
            let curr_user_index = list_of_players.indexOf(player.user)
            console.log(curr_user_index)
            let distance = Math.abs(curr_user_index - logged_in_user_index)
            let seat_index
            if (curr_user_index < logged_in_user_index){
                // curr user on the right of the logged in user
                seat_index = 1 + distance
            }
            // if logged_in_user_index < curr user index, curr user on the left
            else if (logged_in_user_index < curr_user_index){
                seat_index = 7 - distance
            } else{
                seat_index = 1
            }
        if (player.user == game_info['current_player_user']){
            let highlightCurrentPlayer
            console.log(seat_index)
            highlightCurrentPlayer = document.getElementById(`pfp${seat_index}_div`)
            highlightCurrentPlayer.style.boxShadow = "0px 0px 10px 5px #B7D1FF"
        }
        else{
            let highlightCurrentPlayer
            console.log(seat_index)
            highlightCurrentPlayer = document.getElementById(`pfp${seat_index}_div`)
            highlightCurrentPlayer.style.boxShadow = "none"
        }
        
        
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
    let logo = document.getElementById('logo')
    logo.textContent = `${myUserName} IS READY`;
    logo.style.textTransform = "uppercase"
    logo.style.color = "#FFF"
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

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
}

