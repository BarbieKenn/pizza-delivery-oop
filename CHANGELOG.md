# Changelog
All significant changes will be fixed in this file.


[0.1.0]
Initial project structure with `src/` layout and tests.
Defined core domain interfaces:
`order.py`: Order, OrderItem, OrderUnit with status transitions.
`status.py`: OrderStatus state machine.
`products.py`: Pizza, Topping, recipe requirements.
`pricing.py`: PricingStrategy protocols and strategies (NoDiscount, PercentOff, BuyNGetMFree, FirstOrderCoupon).
`inventory.py`: Ingredient, Inventory, Oven with reservation flow.
`delivery.py`: Courier, Vehicle, Dispatcher, AssignmentStrategy.
`payment.py`: Payment interface and implementations (Cash, Card, Online).
`repository.py`: OrderRepository and in-memory stub.
`errors.py`: Unified domain errors for all modules.
Added CLI skeleton in `cli/app.py` with commands (`order new`, `add-item`, `bake`, `dispatch`, `pay`, `deliver`, etc.).
Added test stubs for pricing, inventory/oven, delivery, repository/payment, and integration scenarios.
