# Enhanced populate script with better demo data
# Run: python manage.py runscript enhanced_populate

import os
import sqlite3
import shutil
from django.contrib.auth.models import User
from django.core.files import File
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from website.models import Product, UserDetails, Auction


def run():
    print("🚀 Starting enhanced database population...")
    
    # Clear existing data
    Product.objects.all().delete()
    Auction.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    UserDetails.objects.all().delete()
    
    # Reset sequences
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='website_product'")
    c.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='website_auction'")
    c.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='auth_user'")
    c.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='website_userdetails'")
    conn.commit()
    conn.close()
    
    # Recreate media directory
    try:
        if os.path.exists('media/images/'):
            # Remove all files in directory instead of removing directory
            for filename in os.listdir('media/images/'):
                file_path = os.path.join('media/images/', filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
        os.makedirs('media/images/', exist_ok=True)
    except Exception as e:
        print(f"Warning: Could not clean media directory: {e}")
        os.makedirs('media/images/', exist_ok=True)
    
    print("💾 Database cleared and reset!")
    
    # Create demo users
    users_data = [
        {'username': 'alex_seller', 'email': 'alex@example.com', 'first_name': 'Alex', 'last_name': 'Johnson', 'balance': '150.00'},
        {'username': 'maria_tech', 'email': 'maria@example.com', 'first_name': 'Maria', 'last_name': 'Garcia', 'balance': '200.00'},
        {'username': 'john_collector', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Smith', 'balance': '75.00'},
        {'username': 'emma_gamer', 'email': 'emma@example.com', 'first_name': 'Emma', 'last_name': 'Wilson', 'balance': '120.00'},
    ]
    
    created_users = []
    for user_data in users_data:
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password='testpass123',
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        
        # Create UserDetails
        UserDetails.objects.create(
            user_id=user,
            balance=Decimal(user_data['balance']),
            cellphone='+48 123 456 789',
            address='Demo Street 123',
            town='Warsaw',
            post_code='00-001',
            country='Poland'
        )
        created_users.append(user)
    
    print(f"👥 Created {len(created_users)} demo users!")
    
    # Enhanced product data with better descriptions
    products_data = [
        # Books
        {
            'title': 'The Art of Programming',
            'description': 'A comprehensive guide to modern software development practices. Perfect for both beginners and experienced developers.',
            'category': 'BOK',
            'quantity': 3,
            'image': 'console-01.png'
        },
        {
            'title': 'Digital Photography Masterclass',
            'description': 'Learn professional photography techniques from award-winning photographers. Includes practical exercises and tips.',
            'category': 'BOK',
            'quantity': 2,
            'image': 'console-02.png'
        },
        {
            'title': 'Cooking Around the World',
            'description': 'Discover authentic recipes from 50 countries. Beautifully illustrated cookbook with step-by-step instructions.',
            'category': 'BOK',
            'quantity': 4,
            'image': 'game-01.png'
        },
        {
            'title': 'Financial Freedom Guide',
            'description': 'Practical strategies for building wealth and achieving financial independence. Written by successful investors.',
            'category': 'BOK',
            'quantity': 1,
            'image': 'game-02.png'
        },
        
        # Toys
        {
            'title': 'LEGO Architecture Set',
            'description': 'Build famous landmarks with this premium LEGO set. Includes detailed instruction manual and collector information.',
            'category': 'TOY',
            'quantity': 2,
            'image': 'gadget-01.png'
        },
        {
            'title': 'Remote Control Racing Drone',
            'description': 'High-speed racing drone with 4K camera and advanced stabilization. Perfect for outdoor adventures.',
            'category': 'TOY',
            'quantity': 1,
            'image': 'gadget-02.png'
        },
        {
            'title': 'Educational Robot Kit',
            'description': 'STEM learning kit that teaches programming and robotics. Suitable for ages 10+. Includes sensors and motors.',
            'category': 'TOY',
            'quantity': 3,
            'image': 'laptop-01.png'
        },
        {
            'title': 'Vintage Board Game Collection',
            'description': 'Rare collection of classic board games from the 1980s. All games are in excellent condition with original boxes.',
            'category': 'TOY',
            'quantity': 1,
            'image': 'laptop-02.png'
        },
        
        # Films
        {
            'title': 'Classic Cinema Collection',
            'description': 'Restored 4K collection of 50 greatest films of all time. Includes director commentaries and behind-the-scenes footage.',
            'category': 'FIL',
            'quantity': 2,
            'image': 'tv-01.png'
        },
        {
            'title': 'Sci-Fi Movie Marathon Box',
            'description': 'Complete collection of cult science fiction films. Features rare editions and exclusive bonus content.',
            'category': 'FIL',
            'quantity': 1,
            'image': 'tv-02.png'
        },
        {
            'title': 'Documentary Series Bundle',
            'description': 'Award-winning nature and history documentaries. Over 100 hours of educational content in high definition.',
            'category': 'FIL',
            'quantity': 3,
            'image': 'console-03.png'
        },
        {
            'title': 'Action Movie Collector Edition',
            'description': 'Limited edition box set with steel cases and exclusive artwork. Includes unreleased deleted scenes.',
            'category': 'FIL',
            'quantity': 1,
            'image': 'console-04.png'
        }
    ]
    
    created_products = []
    for i, product_data in enumerate(products_data):
        try:
            product = Product()
            product.title = product_data['title']
            product.description = product_data['description']
            product.quantity = product_data['quantity']
            product.category = product_data['category']
            product.owner = created_users[i % len(created_users)]  # Distribute among users
            
            # Copy image from static folder to media folder
            static_image_path = f'website/static/images/products/{product_data["image"]}'
            if os.path.exists(static_image_path):
                product.image.save(
                    product_data["image"], 
                    File(open(static_image_path, 'rb'))
                )
            
            product.save()
            created_products.append(product)
            
        except Exception as e:
            print(f"❌ Error creating product {product_data['title']}: {e}")
    
    print(f"📦 Created {len(created_products)} products!")
    
    # Create auctions with varied timing
    auction_timings = [
        {'start_offset': -30, 'duration': 60},  # Started 30 min ago, runs for 1 hour
        {'start_offset': -15, 'duration': 45},  # Started 15 min ago, runs for 45 min
        {'start_offset': 5, 'duration': 90},    # Starts in 5 min, runs for 1.5 hours
        {'start_offset': 10, 'duration': 120},  # Starts in 10 min, runs for 2 hours
        {'start_offset': -5, 'duration': 30},   # Started 5 min ago, runs for 30 min
        {'start_offset': 15, 'duration': 60},   # Starts in 15 min, runs for 1 hour
        {'start_offset': -45, 'duration': 90},  # Started 45 min ago, runs for 1.5 hours
        {'start_offset': 30, 'duration': 180},  # Starts in 30 min, runs for 3 hours
        {'start_offset': -10, 'duration': 40},  # Started 10 min ago, runs for 40 min
        {'start_offset': 60, 'duration': 240},  # Starts in 1 hour, runs for 4 hours
        {'start_offset': -20, 'duration': 75},  # Started 20 min ago, runs for 75 min
        {'start_offset': 45, 'duration': 150}   # Starts in 45 min, runs for 2.5 hours
    ]
    
    created_auctions = []
    for i, product in enumerate(created_products):
        if i < len(auction_timings):
            timing = auction_timings[i]
            
            auction = Auction()
            auction.owner = product.owner
            auction.product_id = product
            auction.number_of_bids = 0
            auction.time_starting = timezone.now() + timedelta(minutes=timing['start_offset'])
            auction.time_ending = auction.time_starting + timedelta(minutes=timing['duration'])
            auction.save()
            
            created_auctions.append(auction)
    
    print(f"🎯 Created {len(created_auctions)} auctions!")
    print("✨ Enhanced database population completed!")
    print("\n📊 Summary:")
    print(f"   👥 Users: {len(created_users)}")
    print(f"   📦 Products: {len(created_products)}")
    print(f"   🎯 Auctions: {len(created_auctions)}")
    print("\n🔑 Demo Login Credentials:")
    print("   Username: alex_seller | Password: testpass123")
    print("   Username: maria_tech | Password: testpass123")
    print("   Username: john_collector | Password: testpass123")
    print("   Username: emma_gamer | Password: testpass123")
    print("\n🌐 Visit: http://127.0.0.1:8000/website/")