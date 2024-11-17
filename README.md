# Project: Information Management System for Student Clubs

## (An Implementation of CSC3170 Database Course Final Project with Flask & PyMySQL)

Time Cost: 4 days from scratch ~

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
   - Delete a club (Not Implemented. Looks easy :P)
   - Publish announcement (Not Implemented. Maybe can try another layout :P)
 - [ClubAdmin] 
   - Update club description
   - Publish an event
   - Update an event
   - Compute statistics of students in events
   - Provide search function for students' information
 - [Student] 
   - Query profile
   - Query club membership
   - Query past events
   - Update profile
   - Join an event
   - Join a club
   ...
 
