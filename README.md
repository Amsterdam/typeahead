Typeahead service 
==

Typeahead is een multiplexer die informatie van verschillende backends combineert om één uniforme typeahead in Atlas
mogelijk te maken. Typeahead zorgt voor de ontkoppeling van verschillende service daar waar search over alle services
nodig is.

Deze service is afhankelijk van Consul (http://consul.io). Indien er geen parameters worden meegegeven wordt er een 
Consul http api verwacht. De hostname en poort waar UWSGI naar verbindt hangt af van twee omgevingsvariabelen:
 - CONSUL_HOST (default: consul.service.consul)
 - CONSUL_PORT (default: 8500)
 
 Het is voor development mogelijk om deze Consul node direct in docker te starten met:
 
    `docker run -p 8500:8500/tcp --name=dev-consul consul agent -dev -ui -client 0.0.0.0`
 
 Het interne IP adres van de consul node is te vinden met het volgende commando:
    
    `docker inspect dev-consul | jq '.[] | .NetworkSettings.IPAddress'`
 
 dit ip adres kan vervolgens worden meegegeven bij het starten van de container:
 Bijvoorbeeld indien consul op 172.17.0.2 draait: `CONSUL_HOST=172.17.0.2 docker-compose up` Dit is mogelijk omdat 
 typeahead net als consul aan de bridge interface van docker wordt gekoppeld en niet zoals sinds de v2 config standaard
 is aan een eigen netwerk per docker-compose file.
 
 Voor het draaien van typeahead buiten docker is Consul niet nodig.