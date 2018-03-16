#include "eyefinder.h"

// ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
// *****
// ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
// *****
/*
PUBLIC
*/

_EF_::EyeFinder::EyeFinder(void) : cap(0), abs_ffv{}, rois{} {
  // set the buffersize of cv::VideoCapture -> cap
  cap.set(CV_CAP_PROP_BUFFERSIZE, 3);

  // Initialize the Semaphore (POSIX semaphore)
  sem = sem_open(sem_name, O_CREAT | O_EXCL, 0666, 1);
  if (sem == SEM_FAILED) {
    std::cout << "*** *** sem_open failed!!!" << std::endl;
    std::cout << sem_name << ", errno: " << errno << std::endl;
    sem = sem_open(sem_name, O_CREAT, 0666, 1);
    sem_close(sem);
    exit(1);
  } else {
    printf("sem: %p\n", sem);
  }

  // Initialize the Shared Memory (System V shared Memory)
  // Setup shared memory
  if ((shmid = shmget(key, shared_size, IPC_EXCL | IPC_CREAT | 0666)) < 0) {
    std::cout << "*** *** shmget() failed!!! " << errno << std::endl;
    exit(1);
  } else { // GOLDEN!!!
    std::cout << "shmid: " << shmid << std::endl;
  }
  // Attached shared memory
  if ((shared_memory = (char *)shmat(shmid, NULL, 0)) == (char *)-1) {
    printf("Error attaching shared memory id");
    exit(1);
  } else { // GOLDEN!!!
    std::cout << "shared_memory: " << (unsigned long)shared_memory << std::endl;
  }
}
_EF_::EyeFinder::~EyeFinder(void) {
  // Free the Semaphore
  sem_unlink(sem_name);
  sem_close(sem);
  // Free the Shared Memory
  shmdt(shared_memory);
  shmctl(shmid, IPC_RMID, NULL);

  // Bye message
  std::cout << "\n\nBye~~~!\n" << std::endl;
}

// *****
// start
int _EF_::EyeFinder::start(void) {
  try {
    std::chrono::steady_clock::time_point begin, end;

    if (!cap.isOpened()) {
      std::cerr << "Unable to connect to camera" << std::endl;
      return 1;
    }

    // Load face detection and pose estimation models.
    dlib::frontal_face_detector detector = dlib::get_frontal_face_detector();
    dlib::shape_predictor pose_model;
    dlib::deserialize("shape_predictor_68_face_landmarks.dat") >> pose_model;

    // Grab and process frames until the main window is closed by the user.
#if EF_DEBUG
    int i = 0;
    cv::namedWindow("LALALA", cv::WINDOW_AUTOSIZE);
    while (i++ < 100) {
#else
    while (true) {
#endif
#if EF_DEBUG_PUPIL
      cv::namedWindow("PupilL", cv::WINDOW_AUTOSIZE);
      cv::namedWindow("PupilR", cv::WINDOW_AUTOSIZE);
      cv::namedWindow("PupilL_ACC", cv::WINDOW_AUTOSIZE);
      cv::namedWindow("PupilR_ACC", cv::WINDOW_AUTOSIZE);
#endif
      // Grab a frame
      cv::Mat temp;
      if (!cap.read(temp)) {
        break;
      }

      // Shrink the frame size
      cv::resize(temp, temp, cv::Size(), 0.5, 0.5);
      cv::cvtColor(temp, temp, CV_BGR2GRAY);
      std::pair<int, int> screen_size = std::make_pair(temp.rows, temp.cols);

      dlib::cv_image<dlib::uint8> cimg(temp);

      // Detect faces
      std::vector<dlib::rectangle> faces = detector(cimg);

      // Find the pose of each face. (Only the first)
      std::vector<dlib::full_object_detection> shapes;
      for (unsigned long i = 0; i < 1 && i < faces.size(); ++i)
        shapes.push_back(pose_model(cimg, faces[i]));

      // guarantee that there are at least
      if (shapes.size()) {

        std::vector<double> facial_features_vec;

        // Left eye + Right eye points
        preCalculationPoints(shapes, facial_features_vec, screen_size);

        // calculatePupils(roi_l_mat, facial_features_vec);
        // calculatePupils(roi_r_mat, facial_features_vec);
        // Calling EyeLike's now
        calculatePupilsEL(shapes, facial_features_vec, temp);

        // Find the face angle + pupils
        calculateFaceAngles(shapes, facial_features_vec);

        // Check Correctness of Pupils.
        // TODO.. Need to clear abs_ffv if bad Pupils
        //     Need to use ROI and pupils
        // Pseudo: if (chkisbad) {abs_ffv.clear(); continue;}
        if (ischkbad()) {abs_ffv.clear(); continue;}

        // Write out the Facial Features
        writeFacialFeaturesToShm(facial_features_vec);
        abs_ffv.clear();

      } else {
        writeBadFacialFeaturesToShm(); // or skip it
      }
    }
  } catch (dlib::serialization_error &e) {
    std::cout << "You need dlib's default face landmarking model file to run "
                 "this example."
              << std::endl;
    std::cout << "You can get it from the following URL: " << std::endl;
    std::cout
        << "   http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
        << std::endl;
    std::cout << std::endl << e.what() << std::endl;
  } catch (std::exception &e) {
    std::cout << e.what() << std::endl;
  }
  return 0;
}

// ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
// *****
// ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
// *****
/*
PRIVATE
*/

// *****
// ischkbad
bool _EF_::EyeFinder::ischkbad(void) {
  using XY = std::pair<double,double>;

  cv::Rect l_eye_roi = rois[0], r_eye_roi = rois[1];
  double l_pupil_x = abs_ffv[24], l_pupil_y = abs_ffv[25];
  double r_pupil_x = abs_ffv[26], r_pupil_y = abs_ffv[27];

  auto mmfinder = [this](int l, int r, int step = 2) -> std::pair<XY, XY> {
    XY min_xy = {abs_ffv[l], abs_ffv[l + 1]};
    XY max_xy = min_xy;
    int i;
    for (i = l; i < r; i += step) {
      min_xy.first = std::min(min_xy.first, abs_ffv[i]);
      min_xy.second = std::min(min_xy.second, abs_ffv[i + 1]);
      max_xy.first = std::max(max_xy.first, abs_ffv[i]);
      max_xy.second = std::max(max_xy.second, abs_ffv[i + 1]);
    }
    return {min_xy, max_xy};
  };
  std::pair<XY, XY> l_eye = mmfinder(0, 11);
  std::pair<XY, XY> r_eye = mmfinder(12, 23);

  double l_pupil_x_loc = l_pupil_x + l_eye_roi.x, l_pupil_y_loc = l_pupil_y + l_eye_roi.y;
  double r_pupil_x_loc = r_pupil_x + r_eye_roi.x, r_pupil_y_loc = r_pupil_y + r_eye_roi.y;
  //
  // return l_pupil_x_loc >= l_eye.first.first
  // && l_pupil_x_loc <= l_eye.second.first
  // && l_pupil_y_loc >= l_eye.first.second
  // && l_pupil_y_loc <= l_eye.second.second
  //
  // && r_pupil_x_loc >= r_eye.first.first
  // && r_pupil_x_loc <= r_eye.second.first
  // && r_pupil_y_loc >= r_eye.first.second
  // && r_pupil_y_loc <= r_eye.second.second;

  // Debug
  // std::cout << "l_pupil_x/y_loc  " << l_pupil_x_loc << " " << l_pupil_y_loc << std::endl;
  // std::cout << "r_pupil_x/y_loc  " << r_pupil_x_loc << " " << r_pupil_y_loc << std::endl;
  // std::cout << "l_min/max _x     " << l_eye.first.first << " " << l_eye.second.first << std::endl;
  // std::cout << "r_min/max _x     " << r_eye.first.first << " " << r_eye.second.first << std::endl << std::endl;
  return false; // Temporary
}

// *****
// setMinAndMax
std::tuple<long, long, long, long> _EF_::EyeFinder::setMinAndMax(
    int start, int end,
    const std::vector<dlib::full_object_detection> &shapes) {
  // min_x, min_y, max_x, max_y
  std::tuple<long, long, long, long> tp{LONG_MAX, LONG_MAX, LONG_MIN, LONG_MIN};

  for (int i = start; i <= end; ++i) {
    auto x = shapes[0].part(i).x();
    auto y = shapes[0].part(i).y();
    std::get<0>(tp) = std::min(std::get<0>(tp), x);
    std::get<1>(tp) = std::min(std::get<1>(tp), y);
    std::get<2>(tp) = std::max(std::get<2>(tp), x);
    std::get<3>(tp) = std::max(std::get<3>(tp), y);
  }

  return tp;
}

// *****
// getROI
cv::Rect _EF_::EyeFinder::getROI(std::tuple<long, long, long, long> &tp,
                                 cv::Mat frame) {
  auto start_x = std::max(std::get<0>(tp) - 10, long(0));
  auto start_y = std::max(std::get<1>(tp) - 10, long(0));
  auto size_x =
      std::min(std::get<2>(tp) - std::get<0>(tp) + 15, frame.cols - start_x);
  auto size_y =
      std::min(std::get<3>(tp) - std::get<1>(tp) + 15, frame.rows - start_y);
  return cv::Rect(start_x, start_y, size_x, size_y);
}

// ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
// *****
//
// Calculation!!! (finding face angles, pupils, and writing out to shared
// memory)
//
// ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
// *****

// *****
// preCalculationPoints
//  0-11 = x, y coordinates of left eye points
//  12-23 = x, y coordinates of right eye points
void _EF_::EyeFinder::preCalculationPoints(
    const std::vector<dlib::full_object_detection> &shapes,
    std::vector<double> &facial_features_vec,
    std::pair<int, int> &screen_size) {

  for (int i = 36; i <= 47; ++i) {
    auto shp = shapes[0].part(i);
    double x_val = (double)shp.x() / screen_size.second;
    double y_val = (double)shp.y() / screen_size.first;
    facial_features_vec.push_back(x_val);
    facial_features_vec.push_back(y_val);
    abs_ffv.push_back(shp.x());
    abs_ffv.push_back(shp.y());
  }
}

// *****
// calculateFaceAngles()
void _EF_::EyeFinder::calculateFaceAngles(
    const std::vector<dlib::full_object_detection> &shapes,
    std::vector<double> &facial_features_vec) {
  auto left_cheek = shapes[0].part(1);
  auto right_cheek = shapes[0].part(16);
  auto nose_center = shapes[0].part(33);

  float face_width = right_cheek.x() - left_cheek.x();
  float nose_length = face_width * 0.25;

  float true_center_nose_x = left_cheek.x() + face_width / 2.0;
  float nose_x_offset = nose_center.x() - true_center_nose_x;

  float theta = 0.0;
  if (nose_x_offset != 0.0) {
    float angle = atan(nose_length / std::abs(nose_x_offset));

    theta = (90 - angle * (180.0 / M_PI));
    if (signbit(nose_x_offset))
      theta *= -1;
#if EF_DEBUG_FA
    std::cout << "angle: " << angle << std::endl;
    std::cout << "theta: " << theta << std::endl;
#endif
  }

  float vertical_cheek_offset = right_cheek.y() - left_cheek.y();
  float angle = atan(std::abs(vertical_cheek_offset) / face_width);
  float alpha = angle * (180.00 / M_PI);
  if (signbit(vertical_cheek_offset))
    alpha *= -1;

  // TODO: handle types for theta and alpha
  facial_features_vec.push_back(theta);
  facial_features_vec.push_back(alpha);
  abs_ffv.push_back(theta);
  abs_ffv.push_back(alpha);
}

// *****
// calculatePupilsEL() a.k.a. Timm-Barth Algorithm using EyeLike
void _EF_::EyeFinder::calculatePupilsEL(
    const std::vector<dlib::full_object_detection> &shapes,
    std::vector<double> &facial_features_vec, cv::Mat temp) {

  // left eye + right eye
  std::tuple<long, long, long, long> l_tp =
      EyeFinder::setMinAndMax(36, 41, shapes);
  std::tuple<long, long, long, long> r_tp =
      EyeFinder::setMinAndMax(42, 47, shapes);
  std::tuple<long, long, long, long> face_tp =
      EyeFinder::setMinAndMax(1, 47, shapes);

  // ROI for left eye + right eye
  cv::Rect roi_l = EyeFinder::getROI(l_tp, temp);
  cv::Rect roi_r = EyeFinder::getROI(r_tp, temp);
  cv::Rect roi_face = EyeFinder::getROI(face_tp, temp);
  this->rois.push_back(roi_l);
  this->rois.push_back(roi_r);

  // Display eye tracking on the screen
  cv::Mat roi_l_mat, roi_r_mat, roi_face_mat, roi_l_mat_acc, roi_r_mat_acc;
  roi_l_mat = temp(roi_l);
  roi_r_mat = temp(roi_r);
  roi_face_mat = temp(roi_face);
  roi_l_mat_acc = roi_l_mat.clone();
  roi_r_mat_acc = roi_r_mat.clone();

  cv::Mat temp_clone = temp.clone();
  cv::GaussianBlur(temp_clone, temp_clone, cv::Size(0, 0),
                   0.005 * roi_face.width);
  cv::Point leftPupil = findEyeCenter(temp_clone, roi_l, "Left Eye");
  cv::Point rightPupil = findEyeCenter(temp_clone, roi_r, "Right Eye");

  cv::Mat face_clone = roi_face_mat.clone();
  cv::Rect roi_l_acc(
      cv::Point(roi_l.x - roi_face.x, std::abs(roi_l.y - roi_face.y)),
      roi_l.size());
  cv::Rect roi_r_acc(
      cv::Point(roi_r.x - roi_face.x, std::abs(roi_r.y - roi_face.y)),
      roi_r.size());
  cv::GaussianBlur(face_clone, face_clone, cv::Size(0, 0),
                   0.015 * roi_face.width);
  cv::Point leftPupil_acc = findEyeCenter(face_clone, roi_l_acc, "Left Eye");
  cv::Point rightPupil_acc = findEyeCenter(face_clone, roi_r_acc, "Right Eye");
#if EF_DEBUG
  printf(" ::: %d %d\n", roi_l_acc.x, roi_l_acc.y);
#endif

  // Old...
  // double left_pupil_x = (double)leftPupil.x / roi_l.width;
  // double left_pupil_y = (double)leftPupil.y / roi_l.height;
  // double right_pupil_x = (double)rightPupil.x / roi_r.width;
  // double right_pupil_y = (double)rightPupil.y / roi_r.height;

  double left_pupil_x = (double)leftPupil_acc.x / roi_l.width;
  double left_pupil_y = (double)leftPupil_acc.y / roi_l.height;
  double right_pupil_x = (double)rightPupil_acc.x / roi_r.width;
  double right_pupil_y = (double)rightPupil_acc.y / roi_r.height;

  facial_features_vec.push_back(left_pupil_x);
  facial_features_vec.push_back(left_pupil_y);
  facial_features_vec.push_back(right_pupil_x);
  facial_features_vec.push_back(right_pupil_y);
  abs_ffv.push_back(leftPupil_acc.x);
  abs_ffv.push_back(leftPupil_acc.y);
  abs_ffv.push_back(rightPupil_acc.x);
  abs_ffv.push_back(rightPupil_acc.y);

#if EF_DEBUG_TB
  int real_leftPupil_x = leftPupil.x + roi_l.x;
  int real_leftPupil_y = leftPupil.y + roi_l.y;
  int real_rightPupil_x = rightPupil.x + roi_r.x;
  int real_rightPupil_y = rightPupil.y + roi_r.y;
  cv::circle(temp, cv::Point(real_leftPupil_x, real_leftPupil_y), 1,
             cv::Scalar(255, 255, 255, 255));
  cv::circle(temp, cv::Point(real_rightPupil_x, real_rightPupil_y), 1,
             cv::Scalar(255, 255, 255, 255));
  // cv::resize(temp, temp, cv::Size(300,300));
  cv::imshow("LALALA", temp);
  cv::waitKey(1);

  // left and right eye
  cv::circle(roi_l_mat, cv::Point(leftPupil.x, leftPupil.y), 1,
             cv::Scalar(255, 255, 255, 255));
  cv::circle(roi_r_mat, cv::Point(rightPupil.x, rightPupil.y), 1,
             cv::Scalar(255, 255, 255, 255));
  cv::resize(roi_l_mat, roi_l_mat,
             cv::Size(roi_l_mat.cols * 7, roi_l_mat.rows * 7));
  cv::resize(roi_r_mat, roi_r_mat,
             cv::Size(roi_r_mat.cols * 7, roi_r_mat.rows * 7));
  cv::imshow("PupilL", roi_l_mat);
  cv::imshow("PupilR", roi_r_mat);
  cv::moveWindow("PupilL", 700, 0);
  cv::moveWindow("PupilR", 700, 300);

  // More accurate version...
  cv::circle(roi_l_mat_acc, cv::Point(leftPupil_acc.x, leftPupil_acc.y), 1,
             cv::Scalar(255, 255, 255, 255));
  cv::circle(roi_r_mat_acc, cv::Point(rightPupil_acc.x, rightPupil_acc.y), 1,
             cv::Scalar(255, 255, 255, 255));
  cv::resize(roi_l_mat_acc, roi_l_mat_acc,
             cv::Size(roi_l_mat_acc.cols * 7, roi_l_mat_acc.rows * 7));
  cv::resize(roi_r_mat_acc, roi_r_mat_acc,
             cv::Size(roi_r_mat_acc.cols * 7, roi_r_mat_acc.rows * 7));
  cv::imshow("PupilL_ACC", roi_l_mat_acc);
  cv::imshow("PupilR_ACC", roi_r_mat_acc);
  cv::moveWindow("PupilL_ACC", 1000, 0);
  cv::moveWindow("PupilR_ACC", 1000, 300);
#endif
}

// *****
// writeFacialFeaturesToShm()
//  Will be to shared memory with semaphore synchronization
//  0-11 = x, y coordinates of left eye points
//  12-23 = x, y coordinates of right eye points
//  24, 25 = x, y coordinates of left eye center (timm)
//  26, 27 = x, y coordinates of right eye center (timm)
//  28-29 = face angles (another code)
void _EF_::EyeFinder::writeFacialFeaturesToShm(
    const std::vector<double> &facial_features_vec) {
  int i = 0;
  sem_wait(sem);

  // add an ID to the frame first
  memcpy(shared_memory + sizeof(double) * i, &frame_id, sizeof(double));
  i = 1;

  // now copy every value in vec over
  for (const auto num : facial_features_vec) {
    memcpy(shared_memory + sizeof(double) * i, &num, sizeof(double));
    i++;
  }

  sem_post(sem);
  frame_id = ((int)frame_id + 1) % 100;
}

void _EF_::EyeFinder::writeBadFacialFeaturesToShm(void) {}
