#!/bin/bash

mongoCreds () {
	if [ "$mongoURL" ]; then
		read -p "  Use Existing Mongo Credentials (Y/N): " wantExistingMongoCreds
		if [ "$wantExistingMongoCreds" = "N" ] || [ "$wantExistingMongoCreds" = "n" ]; then
			read -p "  Database Connection URL: " mongoURL
		fi
	else
		read -p "  Database Connection URL: " mongoURL
	fi
}

postgresCreds() {
	if [ "$postgresHost" ]; then
		read -p "  Use Existing Postgres Credentials (Y/N): " wantExistingPostgresCreds
		if [ "$wantExistingPostgresCreds" = "N" ] || [ "$wantExistingPostgresCreds" = "n" ]; then
			read -p "  User: " postgresUser
			read -p "  Host: " postgresHost
			read -p "  Password: " postgresPassword
		fi
	else
		read -p "  User: " postgresUser
		read -p "  Host: " postgresHost
		read -p "  Password: " postgresPassword
	fi
}

couchCreds () {
	if [ "$couchURL" ]; then
		read -p "  Use Existing Couch/Cloudant Credentials (Y/N): " wantExistingCouchCreds
		if [ "$wantExistingCouchCreds" = "N" ] || [ "$wantExistingCouchCreds" = "n" ]; then
			read -p "  Database Connection URL: " couchURL
		fi
	else
		read -p "  Database Connection URL: " couchURL
	fi
}


echo "Welcome to the Bee Travels Data Generating Script"
echo "Please answer the following options to configure your data:"
echo ""
read -p "Destination Data (Y/N): " wantsDestinationData
if [ "$wantsDestinationData" = "Y" ] || [ "$wantsDestinationData" = "y" ]; then
	read -p "  Generate Destination Data (Y/N): " wantsGenerateDestinationData
	if [ "$wantsGenerateDestinationData" = "Y" ] || [ "$wantsGenerateDestinationData" = "y" ]; then
		generateDestinationData=true
	else
		generateDestinationData=false
	fi
	read -p "  Database (mongodb/postgresdb/couchdb/cloudant): " destinationDatabase
	if [ "$destinationDatabase" = "mongodb" ]; then
		mongoCreds
		echo ""
		echo "Starting Destination data process"
		docker run --net host -e GENERATE_DATA=$generateDestinationData -e DATABASE=mongodb -e MONGO_CONNECTION_URL=$mongoURL beetravels/data-gen-destination:v2.0.0
	elif [ "$destinationDatabase" = "postgresdb" ]; then
		postgresCreds
		echo ""
		echo "Starting Destination data process"
		docker run --net host -e GENERATE_DATA=$generateDestinationData -e DATABASE=postgresdb -e PG_USER=$postgresUser -e PG_HOST=$postgresHost -e PG_PASSWORD=$postgresPassword beetravels/data-gen-destination:v2.0.0
	elif [ "$destinationDatabase" = "couchdb" ] || [ "$destinationDatabase" = "cloudant" ]; then
		couchCreds
		echo ""
		echo "Starting Destination data process"
		docker run --net host -e GENERATE_DATA=$generateDestinationData -e DATABASE=couchdb -e COUCH_CONNECTION_URL=$couchURL beetravels/data-gen-destination:v2.0.0
	fi
	echo "Destination data process complete"
fi
echo ""
read -p "Hotel Data (Y/N): " wantsHotelData
if [ "$wantsHotelData" = "Y" ] || [ "$wantsHotelData" = "y" ]; then
	read -p "  Generate Hotel Data (Y/N): " wantsGenerateHotelData
	if [ "$wantsGenerateHotelData" = "Y" ] || [ "$wantsGenerateHotelData" = "y" ]; then
		generateHotelData=true
	else
		generateHotelData=false
	fi
	read -p "  Database (mongodb/postgresdb/couchdb/cloudant): " hotelDatabase
	if [ "$hotelDatabase" = "mongodb" ]; then
		mongoCreds
		echo ""
		echo "Starting Hotel data process"
		docker run --net host -e GENERATE_DATA=$generateHotelData -e DATABASE=mongodb -e MONGO_CONNECTION_URL=$mongoURL beetravels/data-gen-hotel:v2.0.0
	elif [ "$hotelDatabase" = "postgresdb" ]; then
		postgresCreds
		echo ""
		echo "Starting Hotel data process"
		docker run --net host -e GENERATE_DATA=$generateHotelData -e DATABASE=postgresdb -e PG_USER=$postgresUser -e PG_HOST=$postgresHost -e PG_PASSWORD=$postgresPassword beetravels/data-gen-hotel:v2.0.0
	elif [ "$hotelDatabase" = "couchdb" ] || [ "$hotelDatabase" = "cloudant" ]; then
		couchCreds
		echo ""
		echo "Starting Hotel data process"
		docker run --net host -e GENERATE_DATA=$generateHotelData -e DATABASE=couchdb -e COUCH_CONNECTION_URL=$couchURL beetravels/data-gen-hotel:v2.0.0
	fi
	echo "Hotel data process complete"
fi
echo ""
read -p "Car Rental Data (Y/N): " wantsCarData
if [ "$wantsCarData" = "Y" ] || [ "$wantsCarData" = "y" ]; then
	read -p "  Generate Car Rental Data (Y/N): " wantsGenerateCarData
	if [ "$wantsGenerateCarData" = "Y" ] || [ "$wantsGenerateCarData" = "y" ]; then
		generateCarData=true
	else
		generateCarData=false
	fi
	read -p "  Database (mongodb/postgresdb/couchdb/cloudant): " carDatabase
	if [ "$carDatabase" = "mongodb" ]; then
		mongoCreds
		echo ""
		echo "Starting Car Rental data process"
		docker run --net host -e GENERATE_DATA=$generateCarData -e DATABASE=mongodb -e MONGO_CONNECTION_URL=$mongoURL beetravels/data-gen-cars:v2.0.0
	elif [ "$carDatabase" = "postgresdb" ]; then
		postgresCreds
		echo ""
		echo "Starting Car Rental data process"
		docker run --net host -e GENERATE_DATA=$generateCarData -e DATABASE=postgresdb -e PG_USER=$postgresUser -e PG_HOST=$postgresHost -e PG_PASSWORD=$postgresPassword beetravels/data-gen-cars:v2.0.0
	elif [ "$carDatabase" = "couchdb" ] || [ "$carDatabase" = "cloudant" ]; then
		couchCreds
		echo ""
		echo "Starting Car Rental data process"
		docker run --net host -e GENERATE_DATA=$generateCarData -e DATABASE=couchdb -e COUCH_CONNECTION_URL=$couchURL beetravels/data-gen-cars:v2.0.0
	fi
	echo "Car Rental data process complete"
fi
echo ""
echo "Data generation process complete"