from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for
)

from services.chatbot_service import ChatbotService


chatbot_bp = Blueprint(
    "chatbot_bp",
    __name__
)


# ==========================================================
# CHATBOT PAGE
# ==========================================================

@chatbot_bp.route("/chatbot")
def chatbot_page():

    if "user_id" not in session:

        return redirect(
            url_for("auth_bp.login")
        )

    return render_template(
        "chatbot.html",
        user_name=session.get(
            "user_name",
            "User"
        )
    )


# ==========================================================
# CHAT API
# ==========================================================

@chatbot_bp.route(
    "/chat",
    methods=["POST"]
)
def chat():

    if "user_id" not in session:

        return jsonify({
            "error": "Please login first."
        }), 401

    try:

        data = request.get_json(
            silent=True
        )

        if not data:

            return jsonify({
                "error":
                    "No message received."
            }), 400

        message = data.get(
            "message",
            ""
        )

        if not message.strip():

            return jsonify({
                "error":
                    "Please enter a question."
            }), 400

        # --------------------------------------------------
        # Create chatbot
        # --------------------------------------------------

        chatbot = ChatbotService()

        # --------------------------------------------------
        # Generate response
        # --------------------------------------------------

        reply = chatbot.get_response(
            message
        )

        return jsonify({
            "reply": reply
        })

    except Exception as e:

        print(
            "\nCHATBOT ERROR:"
        )

        print(
            str(e)
        )

        import traceback

        traceback.print_exc()

        return jsonify({
            "error":
                "Unable to process your question."
        }), 500