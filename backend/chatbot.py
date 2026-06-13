import random
import re

# Fake order database
ORDERS = {
    "ORD1001": {"status": "Shipped", "item": "Wireless Headphones", "delivery": "June 15, 2026", "amount": "$49.99"},
    "ORD1002": {"status": "Out for Delivery", "item": "Smart Watch", "delivery": "June 13, 2026", "amount": "$89.99"},
    "ORD1003": {"status": "Delivered", "item": "Laptop Bag", "delivery": "June 10, 2026", "amount": "$24.99"},
    "ORD1004": {"status": "Processing", "item": "Bluetooth Speaker", "delivery": "June 18, 2026", "amount": "$34.99"},
    "ORD1005": {"status": "Cancelled", "item": "Phone Case", "delivery": "—", "amount": "$12.99"},
}

def find_order_id(text):
    """Extract order ID pattern like ORD1001 from text."""
    match = re.search(r'ORD\d{4}', text.upper())
    return match.group(0) if match else None

def get_order_details(order_id):
    order = ORDERS.get(order_id)
    if not order:
        return f"I couldn't find any order with ID {order_id}. Please double-check and try again, or contact support@smartshop.com."

    return (f"📦 Order {order_id}\n"
            f"Item: {order['item']}\n"
            f"Status: {order['status']}\n"
            f"Expected Delivery: {order['delivery']}\n"
            f"Amount: {order['amount']}")


# Enhanced response database
INTENTS = {
    "greeting": {
        "patterns": ["hello", "hi", "hey", "good morning", "good evening", "good afternoon", "sup", "howdy", "greetings"],
        "responses": [
            "Hello! Welcome to SmartSupport. How can I help you today?",
            "Hi there! I'm here to help. What do you need assistance with?",
            "Hey! Great to hear from you. What can I do for you?"
        ]
    },
    "order_status": {
        "patterns": ["where is my order", "track order", "order status", "order tracking", "where is my package", "when will my order arrive", "order not received", "order delayed", "check my order"],
        "responses": [
            "I can help you track your order! Please share your order ID (e.g., ORD1001) and I'll look it up for you.",
            "To track your order, I'll need your order number (format: ORD followed by 4 digits). Could you share that?",
            "Sure! Paste your order ID (like ORD1001) here and I'll check the status right away."
        ]
    },
    "return": {
        "patterns": ["return", "send back", "i want to return", "return product", "return item", "return policy", "how to return", "return request"],
        "responses": [
            "We accept returns within 30 days of purchase! To start a return:\n1. Go to Orders\n2. Select the item\n3. Click 'Return'\nNeed help with anything else?",
            "Returns are easy! Just make sure the item is unused and in original packaging. Want me to initiate a return for you?",
            "Our return window is 30 days. Do you have your order number handy so I can start the process?"
        ]
    },
    "refund": {
        "patterns": ["refund", "money back", "get my money", "refund status", "when will i get refund", "refund not received", "charge", "reimbursement"],
        "responses": [
            "Refunds are processed within 5–7 business days after we receive the returned item. Has your return been picked up yet?",
            "Once your return is approved, the refund goes back to your original payment method in 5–7 business days.",
            "I can check your refund status! Could you share your order number?"
        ]
    },
    "shipping": {
        "patterns": ["shipping", "delivery", "how long", "when will it arrive", "estimated delivery", "express shipping", "free shipping", "shipping cost", "dispatch"],
        "responses": [
            "📦 Shipping options:\n- Standard: 3–5 business days (Free over $50)\n- Express: 1–2 business days ($9.99)\n- Overnight: Next day ($19.99)\n\nWhich works for you?",
            "Standard delivery takes 3–5 business days. We also offer express shipping for urgent orders!",
            "Orders are dispatched within 24 hours on weekdays. Delivery usually takes 3–5 days."
        ]
    },
    "cancel": {
        "patterns": ["cancel", "cancel order", "stop order", "don't want", "cancel my order", "cancellation"],
        "responses": [
            "Orders can be cancelled within 1 hour of placement. Please share your order ID and I'll check if cancellation is still possible.",
            "I can cancel your order if it hasn't been dispatched yet. What's your order number?",
            "To cancel, I need your order number. If it's already shipped, we can arrange a return instead."
        ]
    },
    "payment": {
        "patterns": ["payment", "pay", "credit card", "debit card", "upi", "paypal", "payment failed", "payment issue", "not charged", "double charged", "billing"],
        "responses": [
            "We accept Credit/Debit cards, UPI, PayPal, and Net Banking. Is there a specific payment issue I can help with?",
            "If your payment failed but amount was deducted, it will be auto-refunded in 3–5 business days.",
            "For billing issues, could you describe what happened? I'll do my best to help."
        ]
    },
    "product": {
        "patterns": ["product", "item", "stock", "available", "out of stock", "size", "color", "variant", "specification", "features", "details"],
        "responses": [
            "I'd be happy to help with product details! Which item are you asking about?",
            "You can find full specifications on the product page. Is there something specific you want to know?",
            "If an item shows 'Out of Stock', you can click 'Notify Me' to get an alert when it's back!"
        ]
    },
    "discount": {
        "patterns": ["discount", "coupon", "promo code", "offer", "sale", "deal", "voucher", "cashback", "promocode"],
        "responses": [
            "🎉 Current offers:\n- SAVE10: 10% off on orders above $30\n- FIRST20: 20% off for first-time buyers\n- FREESHIP: Free shipping on any order\n\nApply at checkout!",
            "We have great deals running! Use code SAVE10 for 10% off your next order.",
            "Check our Offers page for the latest deals. New coupons every week!"
        ]
    },
    "complaint": {
        "patterns": ["complaint", "problem", "issue", "wrong item", "damaged", "broken", "not working", "defective", "missing item", "bad quality", "worst", "terrible", "horrible"],
        "responses": [
            "I'm really sorry to hear that! 😔 Please describe the issue and share your order number — I'll escalate this immediately.",
            "That's not acceptable and I sincerely apologize. Could you share photos of the issue along with your order ID?",
            "I understand your frustration and I'm here to make this right. Please share your order number so we can resolve this quickly."
        ]
    },
    "thanks": {
        "patterns": ["thank", "thanks", "thank you", "thankyou", "great", "awesome", "perfect", "helpful", "appreciate"],
        "responses": [
            "You're welcome! 😊 Is there anything else I can help you with?",
            "Happy to help! Don't hesitate to reach out anytime.",
            "Glad I could assist! Have a wonderful day! 🌟"
        ]
    },
    "goodbye": {
        "patterns": ["bye", "goodbye", "see you", "take care", "later", "exit", "quit", "done", "that's all"],
        "responses": [
            "Goodbye! Have a great day! 👋",
            "Take care! We're here 24/7 if you need us. 😊",
            "Bye! Don't hesitate to come back if you need help!"
        ]
    },
    "human_agent": {
        "patterns": ["human", "agent", "real person", "talk to someone", "customer service", "support team", "representative", "live chat"],
        "responses": [
            "I'll connect you with a human agent right away! Please hold for 2–3 minutes. ⏳",
            "Transferring you to our support team now. Average wait time: 2 minutes.",
            "A human agent will be with you shortly! In the meantime, is there anything I can help with?"
        ]
    }
}

DEFAULT_RESPONSES = [
    "I'm not sure I understood that. Could you rephrase or choose from: Orders, Returns, Refunds, Shipping, Payments, Discounts?",
    "Hmm, I didn't quite get that. Try asking about your order, return, refund, or shipping!",
    "I want to help but I need a bit more clarity. Could you describe your issue differently?",
    "For complex issues, you can also reach us at support@smartshop.com or type 'human agent' to talk to someone.",
]

def preprocess(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)  # remove punctuation
    return text

def get_response(user_message):
    # Check for order ID first, regardless of intent
    order_id = find_order_id(user_message)
    if order_id:
        return get_order_details(order_id)

    msg = preprocess(user_message)
    words = msg.split()

    best_intent = None
    best_score = 0

    for intent, data in INTENTS.items():
        score = 0
        for pattern in data["patterns"]:
            pattern_words = pattern.lower().split()
            if all(word in msg for word in pattern_words):
                score = len(pattern_words)
            elif any(word in msg for word in pattern_words):
                score = max(score, 1)

        if score > best_score:
            best_score = score
            best_intent = intent

    if best_intent and best_score > 0:
        return random.choice(INTENTS[best_intent]["responses"])

    return random.choice(DEFAULT_RESPONSES)