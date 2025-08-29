#!/usr/bin/env python3
"""
Initialize sample data for GARG BANDHU inventory system
Run this script to populate the database with construction materials data
"""

from app import app, db
from models import Category, Product, StockMovement
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_categories():
    """Initialize product categories"""
    categories_data = [
        {
            'name': 'Cement',
            'description': 'Ordinary Portland Cement and specialty cement products'
        },
        {
            'name': 'Steel & TMT Bars',
            'description': 'TMT bars, steel rods, and reinforcement materials'
        },
        {
            'name': 'Paints & Coatings',
            'description': 'Interior, exterior paints and protective coatings'
        },
        {
            'name': 'Tile Adhesives & Grouts',
            'description': 'Tile fixing adhesives, grouts, and waterproofing materials'
        },
        {
            'name': 'Construction Tools',
            'description': 'Hand tools, power tools, and construction equipment'
        }
    ]
    
    for cat_data in categories_data:
        existing = Category.query.filter_by(name=cat_data['name']).first()
        if not existing:
            category = Category(**cat_data)
            db.session.add(category)
            logger.info(f"Added category: {cat_data['name']}")
    
    db.session.commit()

def init_products():
    """Initialize sample products"""
    
    # Get categories
    cement_cat = Category.query.filter_by(name='Cement').first()
    steel_cat = Category.query.filter_by(name='Steel & TMT Bars').first()
    paint_cat = Category.query.filter_by(name='Paints & Coatings').first()
    adhesive_cat = Category.query.filter_by(name='Tile Adhesives & Grouts').first()
    tools_cat = Category.query.filter_by(name='Construction Tools').first()
    
    products_data = [
        # Cement Products
        {
            'name': 'UltraTech Ordinary Portland Cement',
            'brand': 'UltraTech',
            'category_id': cement_cat.id,
            'unit': 'Bag',
            'pack_size': '50KG',
            'description': 'High quality OPC cement for all construction needs',
            'current_stock': 150,
            'minimum_stock': 50,
            'cost_price': 350.00,
            'selling_price': 380.00
        },
        {
            'name': 'Amba Shakti Portland Cement',
            'brand': 'Amba Shakti',
            'category_id': cement_cat.id,
            'unit': 'Bag',
            'pack_size': '50KG',
            'description': 'Premium quality cement for superior strength',
            'current_stock': 80,
            'minimum_stock': 30,
            'cost_price': 345.00,
            'selling_price': 375.00
        },
        
        # Steel Products
        {
            'name': 'Kamdhenu TMT Bar Fe 500',
            'brand': 'Kamdhenu',
            'category_id': steel_cat.id,
            'unit': 'Ton',
            'pack_size': '12mm',
            'description': 'High strength TMT bars for earthquake resistant construction',
            'current_stock': 5,
            'minimum_stock': 2,
            'cost_price': 52000.00,
            'selling_price': 54000.00
        },
        {
            'name': 'Kamdhenu TMT Bar Fe 500',
            'brand': 'Kamdhenu',
            'category_id': steel_cat.id,
            'unit': 'Ton',
            'pack_size': '16mm',
            'description': 'High strength TMT bars for heavy construction',
            'current_stock': 3,
            'minimum_stock': 1,
            'cost_price': 52500.00,
            'selling_price': 54500.00
        },
        
        # Paint Products
        {
            'name': 'Berger Weathercoat Long Life',
            'brand': 'Berger',
            'category_id': paint_cat.id,
            'unit': 'Bucket',
            'pack_size': '20L',
            'description': 'Premium exterior emulsion paint with 12 year warranty',
            'current_stock': 25,
            'minimum_stock': 10,
            'cost_price': 3200.00,
            'selling_price': 3500.00
        },
        {
            'name': 'Berger Silk Glamour Interior Paint',
            'brand': 'Berger',
            'category_id': paint_cat.id,
            'unit': 'Bucket',
            'pack_size': '20L',
            'description': 'Luxury silk finish interior emulsion paint',
            'current_stock': 18,
            'minimum_stock': 8,
            'cost_price': 2800.00,
            'selling_price': 3100.00
        },
        
        # Tile Adhesives
        {
            'name': 'UltraTech Tilefixo Super',
            'brand': 'UltraTech',
            'category_id': adhesive_cat.id,
            'unit': 'Bag',
            'pack_size': '20KG',
            'description': 'Premium tile adhesive for wall and floor tiles',
            'current_stock': 40,
            'minimum_stock': 15,
            'cost_price': 420.00,
            'selling_price': 450.00
        },
        {
            'name': 'Birla Opus Tile Grout',
            'brand': 'Birla Opus',
            'category_id': adhesive_cat.id,
            'unit': 'Bag',
            'pack_size': '5KG',
            'description': 'High quality grout for tile joints',
            'current_stock': 60,
            'minimum_stock': 20,
            'cost_price': 180.00,
            'selling_price': 200.00
        },
        
        # Construction Tools
        {
            'name': 'Steel Trowel 10 inch',
            'brand': 'Local',
            'category_id': tools_cat.id,
            'unit': 'Piece',
            'pack_size': '10 inch',
            'description': 'High quality steel trowel for plastering work',
            'current_stock': 12,
            'minimum_stock': 5,
            'cost_price': 120.00,
            'selling_price': 150.00
        },
        {
            'name': 'Spirit Level 2 feet',
            'brand': 'Stanley',
            'category_id': tools_cat.id,
            'unit': 'Piece',
            'pack_size': '2 feet',
            'description': 'Precision spirit level for accurate measurements',
            'current_stock': 8,
            'minimum_stock': 3,
            'cost_price': 450.00,
            'selling_price': 520.00
        }
    ]
    
    for product_data in products_data:
        existing = Product.query.filter_by(
            name=product_data['name'], 
            brand=product_data['brand'],
            pack_size=product_data['pack_size']
        ).first()
        
        if not existing:
            product = Product(**product_data)
            db.session.add(product)
            db.session.commit()
            
            # Add initial stock movement
            if product.current_stock > 0:
                movement = StockMovement(
                    product_id=product.id,
                    movement_type='IN',
                    quantity=product.current_stock,
                    reference='Initial Stock',
                    notes='Initial inventory setup',
                    created_by='System'
                )
                db.session.add(movement)
            
            logger.info(f"Added product: {product_data['name']} - {product_data['brand']}")
    
    db.session.commit()

def main():
    """Initialize all sample data"""
    logger.info("Starting database initialization...")
    
    with app.app_context():
        try:
            # Create tables if they don't exist
            db.create_all()
            
            # Initialize data
            init_categories()
            init_products()
            
            logger.info("Database initialization completed successfully!")
            
            # Print summary
            categories_count = Category.query.count()
            products_count = Product.query.count()
            movements_count = StockMovement.query.count()
            
            logger.info(f"Summary:")
            logger.info(f"- Categories: {categories_count}")
            logger.info(f"- Products: {products_count}")
            logger.info(f"- Stock Movements: {movements_count}")
            
        except Exception as e:
            logger.error(f"Error during initialization: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    main()