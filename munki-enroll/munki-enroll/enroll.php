<?php

// Specify the template source to be copied as an individual template
$source="../manifests/individual_template";

// Get the varibles passed by the enroll script
$identifier = $_GET["identifier"];
$hostname   = $_GET["hostname"];

// Create destination
$destination="../manifests/" . $hostname;

// Check if manifest already exists for this machine
if ( file_exists($destination) )
    {
        echo "Computer manifest " . $destination . " already exists.";
    }
else
    {
        echo "Computer manifest does not exist. Will create " . $destination;
    }
?>
