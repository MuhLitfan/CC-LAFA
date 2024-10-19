// Data anggota tim dalam bentuk array of objects
const teamMembers = [
    {
        name: "Nama Anggota 1",
        position: "Posisi 1",
        email: "anggota1@example.com",
        photo: "path_to_photo1.jpg",
        social: {
            facebook: "https://facebook.com",
            twitter: "https://twitter.com",
            linkedin: "https://linkedin.com"
        }
    },
    {
        name: "Nama Anggota 2",
        position: "Posisi 2",
        email: "anggota2@example.com",
        photo: "path_to_photo2.jpg",
        social: {
            facebook: "https://facebook.com",
            twitter: "https://twitter.com",
            linkedin: "https://linkedin.com"
        }
    },
    {
        name: "Nama Anggota 3",
        position: "Posisi 3",
        email: "anggota3@example.com",
        photo: "path_to_photo3.jpg",
        social: {
            facebook: "https://facebook.com",
            twitter: "https://twitter.com",
            linkedin: "https://linkedin.com"
        }
    },
    {
        name: "Nama Anggota 4",
        position: "Posisi 4",
        email: "anggota4@example.com",
        photo: "path_to_photo4.jpg",
        social: {
            facebook: "https://facebook.com",
            twitter: "https://twitter.com",
            linkedin: "https://linkedin.com"
        }
    }
];

// Fungsi untuk membuat elemen anggota tim secara dinamis
function generateTeamMembers() {
    const teamContainer = document.querySelector('.team');
    
    teamMembers.forEach(member => {
        // Buat elemen div untuk profile card
        const profileCard = document.createElement('div');
        profileCard.classList.add('profile-card');
        
        // Tambahkan foto
        const img = document.createElement('img');
        img.src = member.photo;
        img.alt = `Profile Photo of ${member.name}`;
        img.classList.add('profile-photo');
        profileCard.appendChild(img);
        
        // Tambahkan nama
        const nameElement = document.createElement('h2');
        nameElement.classList.add('name');
        nameElement.textContent = member.name;
        profileCard.appendChild(nameElement);
        
        // Tambahkan posisi
        const positionElement = document.createElement('p');
        positionElement.classList.add('position');
        positionElement.textContent = member.position;
        profileCard.appendChild(positionElement);
        
        // Tambahkan email
        const emailElement = document.createElement('p');
        emailElement.classList.add('email');
        emailElement.innerHTML = `Email: <a href="mailto:${member.email}">${member.email}</a>`;
        profileCard.appendChild(emailElement);
        
        // Tambahkan media sosial
        const socialDiv = document.createElement('div');
        socialDiv.classList.add('social-media');
        socialDiv.innerHTML = `
            <a href="${member.social.facebook}" target="_blank">Facebook</a> |
            <a href="${member.social.twitter}" target="_blank">Twitter</a> |
            <a href="${member.social.linkedin}" target="_blank">LinkedIn</a>
        `;
        profileCard.appendChild(socialDiv);
        
        // Masukkan profile card ke container tim
        teamContainer.appendChild(profileCard);
    });
}

// Panggil fungsi untuk membuat anggota tim saat halaman dimuat
document.addEventListener('DOMContentLoaded', generateTeamMembers);
