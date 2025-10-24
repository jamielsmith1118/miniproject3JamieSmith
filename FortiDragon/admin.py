# FortiDragon/admin.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from FortiDragon.auth import login_required
from FortiDragon.admin_auth import admin_required
from FortiDragon.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@login_required
@admin_required
def dashboard():
    db = get_db()
    pending = db.execute(
        '''SELECT p.id, p.title, p.status, u.username
           FROM post p JOIN user u ON p.author_id=u.id
           WHERE p.status IN ('Open','In Review')
           ORDER BY p.id DESC'''
    ).fetchall()
    users = db.execute(
        '''SELECT id, username, role, first_name, last_name, email_address
           FROM user ORDER BY username'''
    ).fetchall()
    return render_template('admin/dashboard.html', pending=pending, users=users)

@bp.post('/post/<int:rid>/approve')
@login_required
@admin_required
def approve_report(rid):
    db = get_db()
    db.execute('UPDATE post SET status = ? WHERE id = ?', ('Approved', rid))
    db.commit()
    flash('Report approved.')
    return redirect(url_for('admin.dashboard'))

@bp.post('/post/approve_all')
@login_required
@admin_required
def approve_all_reports():
    db = get_db()
    cur = db.execute(
        "UPDATE post SET status = 'Approved' WHERE status IN ('Open','In Review')"
    )
    db.commit()
    # cur.rowcount is the number of rows changed
    changed = cur.rowcount if cur.rowcount is not None else 0
    flash(f'Approved {changed} pending report(s).')
    return redirect(url_for('admin.dashboard'))

@bp.post('/post/<int:rid>/reject')
@login_required
@admin_required
def reject_report(rid):
    db = get_db()
    db.execute('UPDATE post SET status = ? WHERE id = ?', ('Rejected', rid))
    db.commit()
    flash('Report rejected.')
    return redirect(url_for('admin.dashboard'))

@bp.post('/post/<int:rid>/delete')
@login_required
@admin_required
def delete_report(rid):
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (rid,))
    db.commit()
    flash('Report deleted.')
    return redirect(url_for('admin.dashboard'))

@bp.post('/users/<int:uid>/role')
@login_required
@admin_required
def change_role(uid):
    new_role = request.form.get('role')
    if new_role not in ('user','admin'):
        flash('Invalid role.')
        return redirect(url_for('admin.dashboard'))
    db = get_db()
    db.execute('UPDATE user SET role = ? WHERE id = ?', (new_role, uid))
    db.commit()
    flash('Role updated.')
    return redirect(url_for('admin.dashboard'))