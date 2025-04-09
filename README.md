Nume: Bolfă Robert-Ion
Grupă: 333 CB

# Tema <1>

Organizare
-
1. Explicație pentru soluția aleasă:

Am implementat un ThreadPool, care lansează un număr de threaduri, fiecare preluând și procesând
taskuri dintr-o coadă partajată. Astfel am obținut o executie unde mai multe cereri pot fi procesate
simultan, fără a recrea threaduri pentru fiecare task. Am decis să îmi mai fac o clasă job manager 
pentru ca eu personal am simțit că e mai natural să folosesc ceva de genul pentru a putea sa fac 
diverse lucruri cu joburile. În task_runner doar am match-uit joburile din coadă cu numele lor,
iar după aceea le-am procesat. Funcțiile le-am păstrat într-un fișier separat pentru a modulariza
codul mai bine.

Personal consider că tema este foarte utilă deoarece unește mai multe arii din programare și
este un exercițiu foarte bun pentru a înțelege cum ar putea funcționa un backend minimal.

Legat de implementare, cred că este destul de echilibrată. ThreadPool-ul este eficient deoarece
folosește threaduri persistente și nu recreează resurse. Probabil că există și posibilități de 
îmbunătățire.

Implementare
-

Nu am implementat Unittests, am făcut doar un test.
Funcționalități extra nu am facut.
Funcționalitățile care nu sunt verificate sunt 3 api-uri /api/num_jobs, /api/jobs și /api/graceful_shutdown
A fost destul de dificil să îmi dau seama cum aș aborda setul de date. Nu știam de existența pandas, mi-a fost recomandat
de un coleg să folosesc asta, de asemenea când apelam anumite funcții în loc să îmi parseze int , îmi parsa string și 
am stat destul de mult pe debug pe chestia asta. De asemenea și configurarea modulului de logging mi s-a părut puțin complicată
având în vedere că a fost prima oară când am făcut asta.
Pe parcurs după cum am spus și mai sus am înțeles să fac unittest-uri (chiar dacă am făcut doar 1), am descoperit și cum pot să
prelucrez așa multe date cu ajutorul pandas și desigur flask.



Resurse utilizate
-
w3school, laburi ASC, stackoverflow, youtube, documentația oficială python

Git
-
1. https://github.com/Robert326/Tema1-Le_Stats_Sportif
