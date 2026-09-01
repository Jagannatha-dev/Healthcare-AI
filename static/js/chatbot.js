/* ==========================================================
   HEALTHCARE AI CHATBOT
   ========================================================== */

document.addEventListener("DOMContentLoaded", function () {

    /* ======================================================
       GET HTML ELEMENTS
       ====================================================== */

    const chatForm =
        document.getElementById("chatForm");

    const userInput =
        document.getElementById("userInput");

    const chatBody =
        document.getElementById("chatBody");

    const micButton =
        document.getElementById("micButton");


    /* ======================================================
       CHECK REQUIRED ELEMENTS
       ====================================================== */

    if (!chatForm) {
        console.error("Chatbot: chatForm not found.");
        return;
    }

    if (!userInput) {
        console.error("Chatbot: userInput not found.");
        return;
    }

    if (!chatBody) {
        console.error("Chatbot: chatBody not found.");
        return;
    }


    /* ======================================================
       GET SEND BUTTON
       ====================================================== */

    const sendButton =
        chatForm.querySelector(
            'button[type="submit"]'
        );


    /* ======================================================
       REQUEST STATUS
       ====================================================== */

    let requestInProgress = false;


    /* ======================================================
       CURRENT TIME
       ====================================================== */

    function getCurrentTime() {

        const now = new Date();

        return now.toLocaleTimeString(
            [],
            {
                hour: "2-digit",
                minute: "2-digit"
            }
        );
    }


    /* ======================================================
       ESCAPE USER TEXT
       ====================================================== */

    function escapeHtml(text) {

        const div =
            document.createElement("div");

        div.textContent =
            String(text);

        return div.innerHTML;
    }


    /* ======================================================
       SCROLL CHAT TO BOTTOM
       ====================================================== */

    function scrollToBottom() {

        requestAnimationFrame(function () {

            chatBody.scrollTop =
                chatBody.scrollHeight;

        });

    }


    /* ======================================================
       ADD USER MESSAGE
       ====================================================== */

    function addUserMessage(message) {

        const messageDiv =
            document.createElement("div");

        messageDiv.className =
            "message user";

        messageDiv.innerHTML = `

            <div class="bubble">

                ${escapeHtml(message)}

                <div class="time">

                    ${getCurrentTime()}

                </div>

            </div>

            <div class="avatar">

            </div>

        `;

        chatBody.appendChild(
            messageDiv
        );

        scrollToBottom();
    }


    /* ======================================================
       ADD BOT MESSAGE
       ====================================================== */

    function addBotMessage(message) {

        const messageDiv =
            document.createElement("div");

        messageDiv.className =
            "message bot";

        messageDiv.innerHTML = `

            <div class="avatar">

                🤖

            </div>

            <div class="bubble">

                <div class="bot-content">

                    ${message}

                </div>

                <div class="time">

                    ${getCurrentTime()}

                </div>

            </div>

        `;

        chatBody.appendChild(
            messageDiv
        );

        scrollToBottom();
    }


    /* ======================================================
       ADD TYPING INDICATOR
       ====================================================== */

    function addTypingMessage() {

        removeTypingMessage();

        const messageDiv =
            document.createElement("div");

        messageDiv.className =
            "message bot";

        messageDiv.id =
            "typingMessage";

        messageDiv.innerHTML = `

            <div class="avatar">

                🤖

            </div>

            <div class="bubble">

                <div class="typing">

                    <span></span>

                    <span></span>

                    <span></span>

                </div>

            </div>

        `;

        chatBody.appendChild(
            messageDiv
        );

        scrollToBottom();
    }


    /* ======================================================
       REMOVE TYPING INDICATOR
       ====================================================== */

    function removeTypingMessage() {

        const typingMessage =
            document.getElementById(
                "typingMessage"
            );

        if (typingMessage) {

            typingMessage.remove();

        }
    }


    /* ======================================================
       SEND MESSAGE
       ====================================================== */

    async function sendMessage() {

        /* -----------------------------------------------
           PREVENT MULTIPLE REQUESTS
           ----------------------------------------------- */

        if (requestInProgress) {

            return;

        }


        /* -----------------------------------------------
           GET MESSAGE
           ----------------------------------------------- */

        const message =
            userInput.value.trim();


        /* -----------------------------------------------
           EMPTY MESSAGE
           ----------------------------------------------- */

        if (!message) {

            userInput.focus();

            return;

        }


        /* -----------------------------------------------
           LOCK REQUEST
           ----------------------------------------------- */

        requestInProgress =
            true;


        if (sendButton) {

            sendButton.disabled =
                true;

        }


        /* -----------------------------------------------
           SHOW USER MESSAGE
           ----------------------------------------------- */

        addUserMessage(
            message
        );


        /* -----------------------------------------------
           CLEAR INPUT
           ----------------------------------------------- */

        userInput.value = "";


        /* -----------------------------------------------
           SHOW TYPING
           ----------------------------------------------- */

        addTypingMessage();


        try {

            console.log(
                "Sending chatbot message:",
                message
            );


            /* ==========================================
               SEND TO FLASK
               ========================================== */

            const response =
                await fetch(
                    "/chat",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json",

                            "Accept":
                                "application/json"
                        },

                        credentials:
                            "same-origin",

                        body:
                            JSON.stringify({
                                message:
                                    message
                            })
                    }
                );


            console.log(
                "Chatbot HTTP status:",
                response.status
            );


            /* ==========================================
               GET SERVER RESPONSE
               ========================================== */

            const responseText =
                await response.text();


            console.log(
                "Chatbot server response:",
                responseText
            );


            /* ==========================================
               REMOVE TYPING
               ========================================== */

            removeTypingMessage();


            /* ==========================================
               SERVER ERROR
               ========================================== */

            if (!response.ok) {

                let errorMessage =
                    "The chatbot server returned an error.";

                try {

                    const errorData =
                        JSON.parse(
                            responseText
                        );

                    if (
                        errorData &&
                        errorData.reply
                    ) {

                        errorMessage =
                            errorData.reply;

                    }

                }
                catch (error) {

                    console.error(
                        "Could not parse error JSON:",
                        error
                    );

                }


                addBotMessage(

                    `
                    <h6>❌ Server Error</h6>

                    <p>
                        ${escapeHtml(
                            errorMessage
                        )}
                    </p>
                    `

                );

                return;

            }


            /* ==========================================
               PARSE JSON
               ========================================== */

            let data;

            try {

                data =
                    JSON.parse(
                        responseText
                    );

            }
            catch (error) {

                console.error(
                    "Invalid JSON returned by Flask:",
                    error
                );


                addBotMessage(

                    `
                    <h6>❌ Response Error</h6>

                    <p>
                        The server returned an
                        invalid response.
                    </p>
                    `

                );

                return;

            }


            /* ==========================================
               BOT RESPONSE
               ========================================== */

            if (
                data &&
                data.reply !== undefined &&
                data.reply !== null
            ) {

                addBotMessage(
                    String(data.reply)
                );

            }
            else {

                addBotMessage(

                    `
                    <h6>🤖 Healthcare AI</h6>

                    <p>
                        No response was received
                        from the chatbot.
                    </p>
                    `

                );

            }

        }
        catch (error) {

            console.error(
                "CHATBOT CONNECTION ERROR:",
                error
            );


            removeTypingMessage();


            addBotMessage(

                `
                <h6>❌ Connection Error</h6>

                <p>
                    Unable to connect to the
                    Healthcare AI chatbot.
                </p>

                <p>
                    Please check that the Flask
                    server is running.
                </p>
                `

            );

        }
        finally {

            requestInProgress =
                false;


            if (sendButton) {

                sendButton.disabled =
                    false;

            }


            userInput.focus();

        }

    }


    /* ======================================================
       FORM SUBMIT
       ====================================================== */

    chatForm.addEventListener(
        "submit",
        function (event) {

            /*
             * THIS IS THE IMPORTANT FIX.
             *
             * Prevent the browser from submitting
             * the form and reloading/jumping to the
             * top of the page.
             */

            event.preventDefault();

            event.stopPropagation();

            sendMessage();

        }
    );


    /* ======================================================
       ENTER KEY
       ====================================================== */

    userInput.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Enter"
                &&
                !event.shiftKey
            ) {

                event.preventDefault();

                event.stopPropagation();

                chatForm.requestSubmit();

            }

        }
    );


    /* ======================================================
       MICROPHONE
       ====================================================== */

    if (micButton) {

        micButton.addEventListener(
            "click",
            function () {

                const SpeechRecognition =
                    window.SpeechRecognition ||
                    window.webkitSpeechRecognition;


                if (!SpeechRecognition) {

                    alert(
                        "Voice input is not supported "
                        + "by this browser."
                    );

                    return;

                }


                const recognition =
                    new SpeechRecognition();


                recognition.lang =
                    "en-IN";


                recognition.interimResults =
                    false;


                recognition.maxAlternatives =
                    1;


                recognition.start();


                recognition.onstart =
                    function () {

                        console.log(
                            "Voice recognition started."
                        );

                    };


                recognition.onresult =
                    function (event) {

                        const transcript =
                            event
                                .results[0][0]
                                .transcript;

                        userInput.value =
                            transcript;

                    };


                recognition.onerror =
                    function (event) {

                        console.error(
                            "Speech recognition error:",
                            event.error
                        );

                    };


                recognition.onend =
                    function () {

                        console.log(
                            "Voice recognition ended."
                        );

                    };

            }
        );

    }


    /* ======================================================
       INITIAL FOCUS
       ====================================================== */

    userInput.focus();

});