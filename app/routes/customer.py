from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import Customer, Contact
from app.forms.customer import CustomerForm, ContactForm

customer_bp = Blueprint('customer', __name__, url_prefix='/customers')

@customer_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    customers = Customer.query.order_by(Customer.name).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('customer/index.html', 
                         title='Клиенты',
                         customers=customers)

@customer_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer(
            name=form.name.data,
            company=form.company.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            status=form.status.data,
            notes=form.notes.data
        )
        db.session.add(customer)
        db.session.commit()
        flash('Клиент успешно добавлен!', 'success')
        return redirect(url_for('customer.view', id=customer.id))
    
    return render_template('customer/form.html', 
                         title='Добавить клиента',
                         form=form)

@customer_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    customer = Customer.query.get_or_404(id)
    form = CustomerForm(obj=customer)
    
    if form.validate_on_submit():
        form.populate_obj(customer)
        db.session.commit()
        flash('Информация о клиенте обновлена!', 'success')
        return redirect(url_for('customer.view', id=customer.id))
    
    return render_template('customer/form.html',
                         title='Редактировать клиента',
                         form=form)

@customer_bp.route('/<int:id>')
@login_required
def view(id):
    customer = Customer.query.get_or_404(id)
    contacts = customer.contacts.all()
    tasks = customer.tasks.all()
    
    return render_template('customer/view.html',
                         title=customer.name,
                         customer=customer,
                         contacts=contacts,
                         tasks=tasks)

@customer_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    flash('Клиент удален!', 'success')
    return redirect(url_for('customer.index'))

# Контакты клиента
@customer_bp.route('/<int:customer_id>/contacts/add', methods=['GET', 'POST'])
@login_required
def add_contact(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    form = ContactForm()
    
    if form.validate_on_submit():
        contact = Contact(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            position=form.position.data,
            email=form.email.data,
            phone=form.phone.data,
            is_primary=form.is_primary.data,
            notes=form.notes.data,
            customer_id=customer.id
        )
        
        if contact.is_primary:
            # Сбрасываем первичный контакт для других контактов этого клиента
            for c in customer.contacts.all():
                c.is_primary = False
        
        db.session.add(contact)
        db.session.commit()
        flash('Контакт добавлен!', 'success')
        return redirect(url_for('customer.view', id=customer.id))
    
    return render_template('customer/contact_form.html',
                         title=f'Добавить контакт для {customer.name}',
                         form=form,
                         customer=customer)

@customer_bp.route('/contacts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_contact(id):
    contact = Contact.query.get_or_404(id)
    customer = contact.customer
    form = ContactForm(obj=contact)
    
    if form.validate_on_submit():
        was_primary = contact.is_primary
        form.populate_obj(contact)
        
        if contact.is_primary and not was_primary:
            # Сбрасываем первичный контакт для других контактов этого клиента
            for c in customer.contacts.all():
                if c.id != contact.id:
                    c.is_primary = False
        
        db.session.commit()
        flash('Контакт обновлен!', 'success')
        return redirect(url_for('customer.view', id=customer.id))
    
    return render_template('customer/contact_form.html',
                         title=f'Редактировать контакт {contact.first_name} {contact.last_name}',
                         form=form,
                         customer=customer)

@customer_bp.route('/contacts/<int:id>/delete', methods=['POST'])
@login_required
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    customer_id = contact.customer_id
    db.session.delete(contact)
    db.session.commit()
    flash('Контакт удален!', 'success')
    return redirect(url_for('customer.view', id=customer_id)) 