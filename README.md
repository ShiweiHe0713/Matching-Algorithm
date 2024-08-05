# Student-Startup Matching Algorithm

First students and startups fill out the Qualtrics and Google forms, then we will extract data from the forms and convert into structured data. With the structured data, then we will do similarity calculation and one-on-one matching. So the input of the program will be the form data, the output will be one on one pairs.

Potentially we will have around 100 startups and 100 MBA students, we will try to matching them evenly.

## Form Design 
Startups will give weights to each feature they want, for example:
- Feature list: []
- Feature weights: []
  
Students also give weights on each feature of their expertise in those field.
- Skill list: []
- Skill level: []

## Cosine similarity calculation
For each company, we calculate the top 10 students based on their cosine similarities. For example:
```csv
Beta Tech,Isaac Rivera,0.9606671410703103,Liam Turner,0.9075950713612995,Oscar Green,0.873333764609373,Daniel Kim,0.8592468124734374,Ethan Mitchell,0.8442226391223938,Lila Harper,0.8442226391223938,Alyssa Nguyen,0.7860003881484358,Catherine Kim,0.7860003881484358,Benjamin Parker,0.7550956836887783,Leo Evans,0.7550956836887783
```

## One-to-One Matching Algorithm
Hugarian algorithm is used in summer 2022, and the Stable Marriage algorithm is going to be used in summer 2024.
