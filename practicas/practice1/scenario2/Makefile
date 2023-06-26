up:
	docker-compose up
upd:
	docker-compose up -d
stop:
	docker-compose stop
restart:
	docker-compose stop && docker-compose up -d
check-ldap:
	docker exec owncloud_ldap_server ldapsearch -x -H ldap://localhost -b dc=modejota,dc=com -D "cn=admin,dc=modejota,dc=com" -w admin
change-passwords:
	docker exec owncloud_ldap_server ldappasswd -x -D "cn=admin,dc=modejota,dc=com" -w admin -s josealberto "uid=josealberto,dc=modejota,dc=com"
	docker exec owncloud_ldap_server ldappasswd -x -D "cn=admin,dc=modejota,dc=com" -w admin -s alberto "uid=alberto,dc=modejota,dc=com"
	docker exec owncloud_ldap_server ldappasswd -x -D "cn=admin,dc=modejota,dc=com" -w admin -s jose "uid=jose,dc=modejota,dc=com"
