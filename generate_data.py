from faker import Faker
import random
import csv
import os

fake = Faker()
NUM_ROWS = 200
OUTPUT_DIR = "ecommerce_dataset"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Define table schemas
schemas = {
    "products": ["id", "name", "description", "brand_id", "category_id"],
    "platforms": ["id", "name", "url", "contact_email"],
    "categories": ["id", "name", "parent_category_id"],
    "brands": ["id", "name", "country"],
    "product_variants": ["id", "product_id", "variant_name", "unit", "size"],
    "platform_products": ["id", "platform_id", "product_id", "sku"],
    "product_prices": ["id", "platform_product_id", "price", "currency", "timestamp"],
    "product_discounts": ["id", "platform_product_id", "discount_percent", "start_date", "end_date"],
    "product_availability": ["id", "platform_product_id", "available", "stock_quantity", "last_checked"],
    "price_history": ["id", "platform_product_id", "price", "checked_at"],

    "users": ["id", "email", "created_at"],
    "user_profiles": ["id", "user_id", "name", "address", "phone"],
    "user_search_history": ["id", "user_id", "query", "searched_at"],
    "user_favorites": ["id", "user_id", "product_id"],
    "user_carts": ["id", "user_id", "created_at"],
    "cart_items": ["id", "cart_id", "product_id", "quantity"],
    "wishlists": ["id", "user_id", "name"],
    "wishlist_items": ["id", "wishlist_id", "product_id"],
    "notifications": ["id", "user_id", "message", "sent_at"],
    "feedback": ["id", "user_id", "message", "submitted_at"],

    "orders": ["id", "user_id", "platform_id", "total_amount", "created_at"],
    "order_items": ["id", "order_id", "product_id", "quantity", "price"],
    "order_status_history": ["id", "order_id", "status", "updated_at"],
    "payment_methods": ["id", "user_id", "method_type", "last_used"],
    "transactions": ["id", "order_id", "status", "transaction_date"],
    "transaction_status": ["id", "transaction_id", "status", "updated_at"],
    "refunds": ["id", "transaction_id", "refund_amount", "refund_date"],
    "shipping_details": ["id", "order_id", "address", "expected_delivery"],
    "delivery_tracking": ["id", "order_id", "status", "updated_at"],
    "delivery_personnel": ["id", "name", "phone", "assigned_area"],

    "price_change_logs": ["id", "platform_product_id", "old_price", "new_price", "changed_at"],
    "discount_change_logs": ["id", "platform_product_id", "old_discount", "new_discount", "changed_at"],
    "availability_logs": ["id", "platform_product_id", "available", "checked_at"],
    "search_logs": ["id", "user_id", "query", "timestamp"],
    "session_logs": ["id", "user_id", "login_time", "logout_time"],
    "query_analytics": ["id", "query", "result_count", "executed_at"],
    "api_usage_logs": ["id", "endpoint", "status_code", "called_at"],
    "platform_response_times": ["id", "platform_id", "response_time_ms", "checked_at"],
    "platform_error_logs": ["id", "platform_id", "error_message", "error_time"],
    "product_ratings": ["id", "product_id", "user_id", "rating", "review"],

    "semantic_categories": ["id", "category_id", "embedding_vector"],
    "query_embeddings": ["id", "query", "embedding_vector"],
    "product_embeddings": ["id", "product_id", "embedding_vector"],
    "recommendation_rules": ["id", "rule_description"],
    "product_similarity_scores": ["id", "product1_id", "product2_id", "similarity_score"],
    "keyword_to_product_mapping": ["id", "keyword", "product_id"],
    "platform_product_mapping_logs": ["id", "platform_product_id", "change_type", "timestamp"],
    "intent_classification_logs": ["id", "query", "intent", "classified_at"],
    "query_feedback_labels": ["id", "query", "label", "labeled_at"],
    "faq_pairs": ["id", "question", "answer"],

    "unit_measurements": ["id", "unit", "description"],
    "delivery_slots": ["id", "platform_id", "slot_start", "slot_end"],
    "geo_locations": ["id", "latitude", "longitude", "location_name"],
    "pincode_mappings": ["id", "pincode", "area_name"],
    "platform_promotions": ["id", "platform_id", "promotion_text", "start_date", "end_date"],
    "coupon_codes": ["id", "code", "discount_percent", "expiry_date"],
    "platform_contacts": ["id", "platform_id", "name", "email", "role"],
    "support_tickets": ["id", "user_id", "subject", "status", "created_at"],
    "app_versions": ["id", "version_number", "release_date"],
    "feature_flags": ["id", "feature_name", "enabled"]
}

# Data generation logic
def generate_row(schema):
    row = []
    for field in schema:
        if field == "id":
            row.append(None)  # ID will be set later
        elif "date" in field or "time" in field:
            row.append(fake.date_time_this_year().isoformat())
        elif "email" in field:
            row.append(fake.email())
        elif "name" in field and "product" not in field and "platform" not in field:
            row.append(fake.name())
        elif "description" in field or "message" in field or "subject" in field or "review" in field:
            row.append(fake.sentence())
        elif "url" in field:
            row.append(fake.url())
        elif "phone" in field:
            row.append(fake.phone_number())
        elif "embedding_vector" in field:
            row.append(str([round(random.uniform(-1, 1), 3) for _ in range(10)]))
        elif "status" in field or "enabled" in field:
            row.append(random.choice(["active", "inactive", "pending", "success", "failed", "true", "false"]))
        elif "quantity" in field or "price" in field or "amount" in field or "percent" in field or "score" in field:
            row.append(round(random.uniform(5, 500), 2))
        elif "currency" in field:
            row.append(random.choice(["INR", "USD"]))
        elif "boolean" in field or "available" in field:
            row.append(random.choice(["true", "false"]))
        elif "code" in field:
            row.append(fake.bothify(text='??##??##'))
        elif "version" in field:
            row.append(fake.numerify(text="v#.#.#"))      # e.g., "v2.3.5"

        else:
            row.append(fake.word())
    return row

# Write CSVs
for table_name, schema in schemas.items():
    rows = []
    for i in range(NUM_ROWS):
        row = generate_row(schema)
        row[0] = i + 1  # set ID
        rows.append(row)

    # Write to CSV
    with open(f"{OUTPUT_DIR}/{table_name}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(schema)
        writer.writerows(rows)

OUTPUT_DIR
