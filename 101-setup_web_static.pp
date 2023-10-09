# Puppet manifest for setting up web servers for web_static deployment

# Update package repositories
exec { 'apt-update':
  command => 'sudo apt update -y',
  path    => '/usr/bin',
}

# Install nginx package
package { 'nginx':
  ensure  => 'installed',
  require => Exec['apt-update'],
}

# Define variables and configurations
$alx_base        = '/data/web_static'
$alx_tests       = "${alx_base}/releases/test"
$alx_shared      = "${alx_base}/shared"
$alx_index       = "${alx_tests}/index.html"
$alx_current     = "${alx_base}/current"
$alx_nginx_sites = '/etc/nginx/sites-available/default'

# Create directories and set ownership
file { [$alx_tests, $alx_shared]:
  ensure => 'directory',
} ->
file { $alx_index:
  ensure  => 'file',
  content => 'Hello World!',
} ->
file { $alx_current:
  ensure  => 'link',
  target  => $alx_tests,
  force   => true,
} ->
exec { 'chown-web-static':
  command => "sudo chown -R ubuntu:ubuntu ${alx_base}",
  path    => '/usr/bin',
  require => File[$alx_tests],
}

# Configure nginx
$nginx_config = "server {
  listen 80 default_server;
  listen [::]:80 default_server;
  add_header X-Served-By $::hostname;
  root   /var/www/html;
  index  index.html index.htm;

  location /hbnb_static/ {
    alias $alx_current;
  }

  location /redirect_me {
    return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
  }

  error_page 404 /404.html;
  location /404 {
    internal;
    root /var/www/html;
  }
}"
file { $alx_nginx_sites:
  ensure  => 'file',
  content => $nginx_config,
  require => Exec['chown-web-static'],
}
# Restart nginx service
service { 'nginx':
  ensure    => 'running',
  enable    => true,
  require   => File[$alx_nginx_sites],
  subscribe => Exec['chown-web-static'],
}
