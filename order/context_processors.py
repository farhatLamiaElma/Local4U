def cart_data(request):
    return {"cart": request.session.get("cart", {})}
