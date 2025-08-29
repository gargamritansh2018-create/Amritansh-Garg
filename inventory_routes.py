from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import Product, Category, StockMovement, Supplier
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard with inventory overview"""
    try:
        # Get inventory statistics
        total_products = Product.query.count()
        low_stock_products = Product.query.filter(Product.current_stock <= Product.minimum_stock).count()
        out_of_stock_products = Product.query.filter(Product.current_stock == 0).count()
        active_categories = Category.query.count()
        
        # Get recent stock movements
        recent_movements = StockMovement.query.order_by(StockMovement.created_at.desc()).limit(10).all()
        
        # Get low stock products
        low_stock_items = Product.query.filter(Product.current_stock <= Product.minimum_stock).all()
        
        stats = {
            'total_products': total_products,
            'low_stock_products': low_stock_products,
            'out_of_stock_products': out_of_stock_products,
            'active_categories': active_categories
        }
        
        return render_template('admin/dashboard.html', 
                             stats=stats, 
                             recent_movements=recent_movements,
                             low_stock_items=low_stock_items)
    except Exception as e:
        logger.error(f"Error loading admin dashboard: {str(e)}")
        flash('Error loading dashboard', 'error')
        return redirect(url_for('index'))

@app.route('/admin/products')
def admin_products():
    """Product management page"""
    try:
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '', type=str)
        category_filter = request.args.get('category', '', type=str)
        
        query = Product.query
        
        if search:
            query = query.filter(Product.name.contains(search) | Product.brand.contains(search))
        
        if category_filter:
            query = query.filter(Product.category_id == category_filter)
        
        products = query.order_by(Product.name).paginate(
            page=page, per_page=20, error_out=False
        )
        
        categories = Category.query.all()
        
        return render_template('admin/products.html', 
                             products=products, 
                             categories=categories,
                             search=search,
                             category_filter=category_filter)
    except Exception as e:
        logger.error(f"Error loading products page: {str(e)}")
        flash('Error loading products', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/products/add', methods=['GET', 'POST'])
def admin_add_product():
    """Add new product"""
    if request.method == 'POST':
        try:
            product = Product(
                name=request.form['name'],
                brand=request.form['brand'],
                category_id=request.form['category_id'],
                unit=request.form['unit'],
                pack_size=request.form['pack_size'],
                description=request.form.get('description', ''),
                current_stock=int(request.form.get('current_stock', 0)),
                minimum_stock=int(request.form.get('minimum_stock', 10)),
                cost_price=float(request.form.get('cost_price', 0)) if request.form.get('cost_price') else None,
                selling_price=float(request.form.get('selling_price', 0)) if request.form.get('selling_price') else None
            )
            
            db.session.add(product)
            db.session.commit()
            
            # Add initial stock movement if stock > 0
            if product.current_stock > 0:
                movement = StockMovement(
                    product_id=product.id,
                    movement_type='IN',
                    quantity=product.current_stock,
                    reference='Initial Stock',
                    notes='Initial inventory setup',
                    created_by='Admin'
                )
                db.session.add(movement)
                db.session.commit()
            
            flash(f'Product "{product.name}" added successfully!', 'success')
            return redirect(url_for('admin_products'))
            
        except Exception as e:
            logger.error(f"Error adding product: {str(e)}")
            db.session.rollback()
            flash('Error adding product. Please try again.', 'error')
    
    categories = Category.query.all()
    return render_template('admin/add_product.html', categories=categories)

@app.route('/admin/products/<int:product_id>/edit', methods=['GET', 'POST'])
def admin_edit_product(product_id):
    """Edit existing product"""
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        try:
            old_stock = product.current_stock
            
            product.name = request.form['name']
            product.brand = request.form['brand']
            product.category_id = request.form['category_id']
            product.unit = request.form['unit']
            product.pack_size = request.form['pack_size']
            product.description = request.form.get('description', '')
            product.minimum_stock = int(request.form.get('minimum_stock', 10))
            product.cost_price = float(request.form.get('cost_price', 0)) if request.form.get('cost_price') else None
            product.selling_price = float(request.form.get('selling_price', 0)) if request.form.get('selling_price') else None
            product.updated_at = datetime.utcnow()
            
            new_stock = int(request.form.get('current_stock', 0))
            
            # If stock changed, create stock movement
            if new_stock != old_stock:
                movement_type = 'IN' if new_stock > old_stock else 'OUT'
                quantity = abs(new_stock - old_stock)
                
                movement = StockMovement(
                    product_id=product.id,
                    movement_type=movement_type,
                    quantity=quantity,
                    reference='Stock Adjustment',
                    notes=f'Stock adjusted from {old_stock} to {new_stock}',
                    created_by='Admin'
                )
                db.session.add(movement)
                product.current_stock = new_stock
            
            db.session.commit()
            flash(f'Product "{product.name}" updated successfully!', 'success')
            return redirect(url_for('admin_products'))
            
        except Exception as e:
            logger.error(f"Error updating product: {str(e)}")
            db.session.rollback()
            flash('Error updating product. Please try again.', 'error')
    
    categories = Category.query.all()
    return render_template('admin/edit_product.html', product=product, categories=categories)

@app.route('/admin/products/<int:product_id>/stock', methods=['POST'])
def admin_update_stock(product_id):
    """Update product stock"""
    try:
        product = Product.query.get_or_404(product_id)
        
        movement_type = request.form['movement_type']
        quantity = int(request.form['quantity'])
        reference = request.form.get('reference', '')
        notes = request.form.get('notes', '')
        
        # Create stock movement
        movement = StockMovement(
            product_id=product.id,
            movement_type=movement_type,
            quantity=quantity,
            reference=reference,
            notes=notes,
            created_by='Admin'
        )
        
        # Update product stock
        if movement_type == 'IN':
            product.current_stock += quantity
        else:
            product.current_stock = max(0, product.current_stock - quantity)
        
        product.updated_at = datetime.utcnow()
        
        db.session.add(movement)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Stock updated successfully',
            'new_stock': product.current_stock
        })
        
    except Exception as e:
        logger.error(f"Error updating stock: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Error updating stock'
        }), 400

@app.route('/admin/categories')
def admin_categories():
    """Category management page"""
    try:
        categories = Category.query.order_by(Category.name).all()
        return render_template('admin/categories.html', categories=categories)
    except Exception as e:
        logger.error(f"Error loading categories: {str(e)}")
        flash('Error loading categories', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/categories/add', methods=['POST'])
def admin_add_category():
    """Add new category"""
    try:
        name = request.form['name']
        description = request.form.get('description', '')
        
        # Check if category already exists
        existing = Category.query.filter_by(name=name).first()
        if existing:
            flash(f'Category "{name}" already exists!', 'error')
            return redirect(url_for('admin_categories'))
        
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        
        flash(f'Category "{name}" added successfully!', 'success')
        return redirect(url_for('admin_categories'))
        
    except Exception as e:
        logger.error(f"Error adding category: {str(e)}")
        db.session.rollback()
        flash('Error adding category. Please try again.', 'error')
        return redirect(url_for('admin_categories'))

@app.route('/admin/reports')
def admin_reports():
    """Inventory reports page"""
    try:
        # Stock status report
        in_stock = Product.query.filter(Product.current_stock > Product.minimum_stock).count()
        low_stock = Product.query.filter(
            Product.current_stock <= Product.minimum_stock,
            Product.current_stock > 0
        ).count()
        out_of_stock = Product.query.filter(Product.current_stock == 0).count()
        
        # Category-wise product count
        category_stats = db.session.query(
            Category.name,
            db.func.count(Product.id).label('product_count')
        ).outerjoin(Product).group_by(Category.id, Category.name).all()
        
        # Recent stock movements (last 30 days)
        from datetime import timedelta
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_movements = StockMovement.query.filter(
            StockMovement.created_at >= thirty_days_ago
        ).order_by(StockMovement.created_at.desc()).limit(50).all()
        
        stock_stats = {
            'in_stock': in_stock,
            'low_stock': low_stock,
            'out_of_stock': out_of_stock
        }
        
        return render_template('admin/reports.html',
                             stock_stats=stock_stats,
                             category_stats=category_stats,
                             recent_movements=recent_movements)
    except Exception as e:
        logger.error(f"Error loading reports: {str(e)}")
        flash('Error loading reports', 'error')
        return redirect(url_for('admin_dashboard'))