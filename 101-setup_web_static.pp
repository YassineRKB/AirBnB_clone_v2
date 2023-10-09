exec { 'aptoperations':
  command => 'apt update && apt -y install nginx',
  provider => shell,
}
-> exec { 'dirs':
  command => 'mkdir -p /data/web_static/releases/test/ && mkdir -p /data/web_static/shared/',
  provider => shell,
}
-> exec { 'greetings':
  command => 'echo "Hello Worldo!" > /data/web_static/releases/test/index.html',
  provider => shell,
}
-> exec { 'slink':
  command => 'ln -sfn /data/web_static/releases/test /data/web_static/current',
  provider => shell,
}
-> exec { 'dataperms':
  command => 'chown -R ubuntu:ubuntu /data/',
  provider => shell,
}
-> exec { 'defaultsites':
  command => 'sudo sed -i "s|server_name _;|server_name _;\n\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}|" /etc/nginx/sites-enabled/default',
  provider => shell,
}
-> exec { 'servicerestart':
  command => 'sudo service nginx restart',
  provider => shell,
}
