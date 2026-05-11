from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app.models.order import Order, PaymentStatus, WorkflowStatus
from app.schemas.order import OrderCreate, OrderResponse
from app.utils.error_handler import handle_workflow_error

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # 1️⃣ Duplicate Order Detection (SRS 3.1.3 FR-5)
    duplicate_window = datetime.utcnow() - timedelta(days=30)
    existing = db.query(Order).filter(
        Order.customer_contact == order.customer_contact,
        Order.product_details == order.product_details,
        Order.created_at >= duplicate_window
    ).first()

    if existing:
        handle_workflow_error(
            db=db, workflow_type="order", entity_id=None,
            step_name="duplicate_detection", error_type="duplicate_entry",
            error_message=f"Duplicate order for {order.customer_contact}",
            is_critical=True
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Duplicate order detected. Workflow paused for manual review."
        )

    # 2️⃣ Payment Failure Exception (SRS 3.1.3 FR-5)
    if order.payment_status == PaymentStatus.failed:
        handle_workflow_error(
            db=db, workflow_type="order", entity_id=None,
            step_name="payment_validation", error_type="payment_failure",
            error_message="Payment failed. Workflow paused for manual approval.",
            is_critical=True
        )
        # Save order but keep it PAUSED
        new_order = Order(
            customer_name=order.customer_name,
            customer_contact=order.customer_contact,
            product_details=order.product_details,
            quantity=order.quantity,
            total_price=order.total_price,
            payment_method=order.payment_method,
            payment_status=order.payment_status,
            workflow_status=WorkflowStatus.paused
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order

    # 3️⃣ Normal Flow (SRS 3.1.3 FR-3)
    new_order = Order(
        customer_name=order.customer_name,
        customer_contact=order.customer_contact,
        product_details=order.product_details,
        quantity=order.quantity,
        total_price=order.total_price,
        payment_method=order.payment_method,
        payment_status=order.payment_status,
        workflow_status=WorkflowStatus.received
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    # TODO: Add email/WhatsApp triggers here (Day 4)
    return new_order