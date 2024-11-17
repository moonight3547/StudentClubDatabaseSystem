# CSC3170 Project: Information Management System for Student Clubs

## Overview

This project is an information management system for student clubs, which allows students to join, manage, and participate in various clubs. The system includes features such as club management, event management, and member management.

## What I use in this project
 - MySQL to provide support of database
 - PyMySQL package for access to MySQL
 - Flask package for backend framework
 - Python as programming language
 - HTML for webpage design at frontend
 - CSS for webpage formatting

## 3 Roles
 - Student: A student who can join clubs, create events, and participate in events.
 - Club Administrator: A club administrator who can manage the club, create events, and manage members.
 - Admin: An administrator who can manage the system, including managing clubs, events, and members.

## Basic Features
- Club management: Admin can create clubs.
- Event management: Club-admin can create / edit events.
- Profile management: Student can update their profile.

## 14 Functions
 - All Account
   - Login
   - Register
 - [Admin] 
   - Create a new club
   - Delete a club
   - Publish announcement
 - [ClubAdmin] 
   - Publish an event
   - Update an event
   - Compute statistics of students in events
     - total number of student
     - students from different grades
     - students from different schools
     - pairs of students with same interest
   - Update club description
 - [Student] 
   - Query profile
   - Query club membership
   - Query past events
   - Update profile
   - Join an event

## Websites
 - "localhost:5000/": index page
 - "localhost:5000/login": login page
 - "localhost:5000/register": register page
 - "localhost:5000/clubs": page with a list of clubs
 - "localhost:5000/clubs/<club>": club page
 - "localhost:5000/clubs/<club>/<event>": event page under club
 - "localhost:5000/profile": profile page for user

## Execution
 - First ... 

    <div class = "layout" style = "text-align: right;">
        <p id = "user">User: {{user}}</p>
    </div>
