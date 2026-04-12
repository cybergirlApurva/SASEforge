package saseforge.authz

# Default deny all
default allow = false

# Allow only authenticated users with correct role
allow {
  input.user.authenticated == true
  input.user.role == "employee"
  input.resource != "restricted-db"
}

# Admins can access everything
allow {
  input.user.authenticated == true
  input.user.role == "admin"
}

# Block all access to DB for non-admins
deny {
  input.resource == "restricted-db"
  input.user.role != "admin"
}
