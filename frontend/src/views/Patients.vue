<template>
  <div class="wrapper-cards">
    <!-- <template v-if="selectedID === ''"> -->
      <div v-for="(profile, index) in profiles" :key="index" class="card" style="width: 18rem;">
        <img class="card-img-top" :src="profile.image" alt="Card image cap">
        <div class="card-body">
          <h5 class="card-title">{{profile.name}}</h5>
          <!-- <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p> -->
          <router-link :to="`/patients/${index + 1}`" exact class="btn btn-primary">Profile</router-link>
        </div>
      </div>

  </div>
</template>

<script>
  import pictureData from '../data.js';
  export default {
    data() {
      return {
        prescriptions: [
          {
            id: 1,
            profileId: 1,
            description: 'drug-id-name',
            dosage: 'One pill a night for 6 weeks',
            prescriptionQRcode: 'string',
            startDate: '02/18/2009',
            endDate: '05/15/2015',
          },
        ],
        profiles: pictureData.profiles,
      };
    },
    mounted() {
      // console.log('db', db);
    },
    methods: {
      _handlePatientProfileLoad(index) {
        this.selectedID = index;
      },
    },
  };
</script>

<style lang="scss">
  .wrapper-cards {
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
    max-width: 1020px;
  }
  .card {
    width: calc(32%-40px);
    border-radius: 20px;
    box-sizing: border-box;
    margin: 15px;
    box-shadow: 0 30px 60px 0 rgba(0, 0, 0, 0.3);
  }
  img {
    object-fit: cover;
    height: 250px;
    width: 150px;
  }
  .card-img-top {
    border-radius: 50%;
    stroke: 3px solid lightblue;
  }
  .card {
    padding: 40px;
  }
</style>