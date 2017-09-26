using System;
using TDAPIOLELib;

namespace AutomatedDefectCreation
{
    public class CreateBug
    {
        public static void Main()
        {
            String qcUrl = "http://qcurl.com:8080/qcbin";
            String qcDomain = ""; // Nearly all our projects are under DEFAULT domain
            String qcProject = ""; // Project we want to log a defect to
            String qcLoginName = ""; // User account we'll use to log it
            String qcPassword = ""; // Password for user account

            TDConnection connection = new TDConnection(); // Open blank connection
            connection.InitConnectionEx(qcUrl); // Go to qcUrl
            connection.ConnectProjectEx(qcDomain, qcProject, qcLoginName, qcPassword); // Validate credentials through API

            BugFactory bugFactory = connection.BugFactory; // Create an object from BugFactory
            Bug newBug = bugFactory.AddItem(System.DBNull.Value); // Create a new blank bug, must convert C# Null object type into value of Null type

            // Set values for mandatory fields in new bug
            // Values are arbitrary
            newBug.Status = "New";
            newBug.AssignedTo = qcLoginName;
            newBug.DetectedBy = qcLoginName;
            newBug.Summary = "This is a test defect";
            newBug["BG_SEVERITY"] = "3-Test";
            newBug["BG_DESCRIPTION"] = "This is a test defect";
            newBug["BG_DETECTED_IN_RCYC"] = 1002; // This takes the Release ID from release module, not the string value of its name, unlike every other field.
            newBug["BG_DETECTION_DATE"] = System.DateTime.Today;

            // Post the bug
            newBug.Post();
        }
    }
}